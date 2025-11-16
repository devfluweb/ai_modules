
"""
Cloudflare R2 Storage Client
Downloads CV files from R2 bucket for extraction
"""

import os
import boto3
from botocore.client import Config as BotoConfig
from botocore.exceptions import ClientError
from typing import Optional
import tempfile
import logging

# Import config from parent directory
import sys
sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))
from config import config

logger = logging.getLogger(__name__)


class R2Client:
    """
    Cloudflare R2 storage client for fetching CV files.
    Uses S3-compatible API via boto3.
    """
    
    def __init__(self):
        """Initialize R2 client with credentials from config"""
        
        if not all([config.R2_ACCOUNT_ID, config.R2_ACCESS_KEY_ID, config.R2_SECRET_ACCESS_KEY]):
            raise ValueError("❌ R2 credentials not configured. Check environment variables.")
        
        self.bucket_name = config.R2_BUCKET_NAME
        self.endpoint_url = config.get_r2_endpoint()
        
        # Create S3-compatible client for R2
        self.s3_client = boto3.client(
            's3',
            endpoint_url=self.endpoint_url,
            aws_access_key_id=config.R2_ACCESS_KEY_ID,
            aws_secret_access_key=config.R2_SECRET_ACCESS_KEY,
            config=BotoConfig(
                signature_version='s3v4',
                region_name='auto'
            )
        )
        
        logger.info(f"✅ R2 Client initialized (bucket: {self.bucket_name})")
    
    def download_file(self, r2_key: str, local_path: Optional[str] = None) -> str:
        """
        Download file from R2 bucket to local filesystem.
        
        Args:
            r2_key: File key in R2 (e.g., "cv_files/candidate_123.pdf")
            local_path: Optional local path. If None, creates temp file.
        
        Returns:
            Path to downloaded local file
        
        Raises:
            FileNotFoundError: If file doesn't exist in R2
            Exception: On download failure
        """
        try:
            # Create temp file if no local path provided
            if not local_path:
                suffix = os.path.splitext(r2_key)[1] or '.pdf'
                temp_file = tempfile.NamedTemporaryFile(
                    delete=False,
                    suffix=suffix,
                    prefix='cv_'
                )
                local_path = temp_file.name
                temp_file.close()
            
            logger.info(f"📥 Downloading from R2: {r2_key}")
            
            # Download file
            self.s3_client.download_file(
                Bucket=self.bucket_name,
                Key=r2_key,
                Filename=local_path
            )
            
            # Verify file exists and has content
            if not os.path.exists(local_path):
                raise Exception(f"Download failed - file not found: {local_path}")
            
            file_size = os.path.getsize(local_path)
            if file_size == 0:
                raise Exception(f"Download failed - empty file: {local_path}")
            
            logger.info(f"✅ Downloaded {file_size} bytes → {local_path}")
            return local_path
            
        except ClientError as e:
            error_code = e.response.get('Error', {}).get('Code', '')
            if error_code == 'NoSuchKey' or error_code == '404':
                logger.error(f"❌ File not found in R2: {r2_key}")
                raise FileNotFoundError(f"File not found in R2 bucket: {r2_key}")
            else:
                logger.error(f"❌ R2 download failed: {e}")
                raise Exception(f"R2 download error: {str(e)}")
        
        except Exception as e:
            logger.error(f"❌ Download failed: {e}")
            raise
    
    def file_exists(self, r2_key: str) -> bool:
        """Check if file exists in R2 bucket"""
        try:
            self.s3_client.head_object(
                Bucket=self.bucket_name,
                Key=r2_key
            )
            return True
        except ClientError:
            return False
    
    def get_file_info(self, r2_key: str) -> dict:
        """Get file metadata from R2"""
        try:
            response = self.s3_client.head_object(
                Bucket=self.bucket_name,
                Key=r2_key
            )
            return {
                "size": response.get('ContentLength', 0),
                "last_modified": response.get('LastModified'),
                "content_type": response.get('ContentType', 'unknown')
            }
        except ClientError as e:
            logger.error(f"❌ Failed to get file info: {e}")
            return {}
    
    def list_files(self, prefix: str = "", max_files: int = 100) -> list:
        """List files in R2 bucket with optional prefix"""
        try:
            response = self.s3_client.list_objects_v2(
                Bucket=self.bucket_name,
                Prefix=prefix,
                MaxKeys=max_files
            )
            
            files = []
            for obj in response.get('Contents', []):
                files.append({
                    "key": obj.get('Key'),
                    "size": obj.get('Size'),
                    "last_modified": obj.get('LastModified')
                })
            
            return files
            
        except ClientError as e:
            logger.error(f"❌ Failed to list files: {e}")
            return []


# Singleton instance
_r2_client = None


def get_r2_client() -> R2Client:
    """Get or create singleton R2 client"""
    global _r2_client
    if _r2_client is None:
        _r2_client = R2Client()
    return _r2_client