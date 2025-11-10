"""File handling utilities with logging support."""

import logging
import shutil
from pathlib import Path
from typing import Union

logger = logging.getLogger(__name__)


class FileOperationError(Exception):
    """Exception raised when file operations fail."""
    pass


class FileHandler:
    """
    Handles file I/O operations with proper error handling and logging.

    Separates file operations from business logic.
    """

    @staticmethod
    def create_directory(path: Union[str, Path], exist_ok: bool = True) -> bool:
        """
        Create a directory.

        Args:
            path: Directory path to create
            exist_ok: If True, don't raise error if directory exists

        Returns:
            True if directory was created, False if it already existed

        Raises:
            FileOperationError: If directory creation fails
        """
        path = Path(path)

        try:
            if path.exists():
                if path.is_dir():
                    logger.info(f"Directory already exists: {path}")
                    return False
                else:
                    raise FileOperationError(f"Path exists but is not a directory: {path}")

            path.mkdir(parents=True, exist_ok=exist_ok)
            logger.info(f"Created directory: {path}")
            return True

        except PermissionError:
            error_msg = f"Permission denied: Unable to create directory '{path}'"
            logger.error(error_msg)
            raise FileOperationError(error_msg)
        except Exception as e:
            error_msg = f"Failed to create directory '{path}': {e}"
            logger.error(error_msg)
            raise FileOperationError(error_msg)

    @staticmethod
    def write_file(
        filepath: Union[str, Path],
        content: str,
        overwrite: bool = False,
        create_parents: bool = True,
    ) -> bool:
        """
        Write content to a file.

        Args:
            filepath: Path to the file
            content: Content to write
            overwrite: If True, overwrite existing file
            create_parents: If True, create parent directories

        Returns:
            True if file was written, False if skipped (file exists and overwrite=False)

        Raises:
            FileOperationError: If file writing fails
        """
        filepath = Path(filepath)

        try:
            if filepath.exists() and not overwrite:
                logger.warning(f"File already exists, skipping: {filepath}")
                return False

            if create_parents:
                filepath.parent.mkdir(parents=True, exist_ok=True)

            filepath.write_text(content, encoding='utf-8')
            logger.info(f"Created file: {filepath}")
            return True

        except PermissionError:
            error_msg = f"Permission denied: Unable to write file '{filepath}'"
            logger.error(error_msg)
            raise FileOperationError(error_msg)
        except Exception as e:
            error_msg = f"Failed to write file '{filepath}': {e}"
            logger.error(error_msg)
            raise FileOperationError(error_msg)

    @staticmethod
    def read_file(filepath: Union[str, Path]) -> str:
        """
        Read content from a file.

        Args:
            filepath: Path to the file

        Returns:
            File content as string

        Raises:
            FileOperationError: If file reading fails
        """
        filepath = Path(filepath)

        try:
            content = filepath.read_text(encoding='utf-8')
            logger.debug(f"Read file: {filepath}")
            return content

        except FileNotFoundError:
            error_msg = f"File not found: {filepath}"
            logger.error(error_msg)
            raise FileOperationError(error_msg)
        except PermissionError:
            error_msg = f"Permission denied: Unable to read file '{filepath}'"
            logger.error(error_msg)
            raise FileOperationError(error_msg)
        except Exception as e:
            error_msg = f"Failed to read file '{filepath}': {e}"
            logger.error(error_msg)
            raise FileOperationError(error_msg)

    @staticmethod
    def copy_file(
        source: Union[str, Path],
        destination: Union[str, Path],
        overwrite: bool = False,
    ) -> bool:
        """
        Copy a file from source to destination.

        Args:
            source: Source file path
            destination: Destination file path
            overwrite: If True, overwrite existing file

        Returns:
            True if file was copied, False if skipped

        Raises:
            FileOperationError: If file copy fails
        """
        source = Path(source)
        destination = Path(destination)

        try:
            if not source.exists():
                raise FileOperationError(f"Source file not found: {source}")

            if destination.exists() and not overwrite:
                logger.warning(f"Destination file already exists, skipping: {destination}")
                return False

            destination.parent.mkdir(parents=True, exist_ok=True)
            shutil.copy2(source, destination)
            logger.info(f"Copied file from {source} to {destination}")
            return True

        except Exception as e:
            error_msg = f"Failed to copy file from '{source}' to '{destination}': {e}"
            logger.error(error_msg)
            raise FileOperationError(error_msg)

    @staticmethod
    def copy_directory(
        source: Union[str, Path],
        destination: Union[str, Path],
        overwrite: bool = False,
    ) -> bool:
        """
        Copy a directory from source to destination.

        Args:
            source: Source directory path
            destination: Destination directory path
            overwrite: If True, overwrite existing directory

        Returns:
            True if directory was copied, False if skipped

        Raises:
            FileOperationError: If directory copy fails
        """
        source = Path(source)
        destination = Path(destination)

        try:
            if not source.exists():
                raise FileOperationError(f"Source directory not found: {source}")

            if not source.is_dir():
                raise FileOperationError(f"Source is not a directory: {source}")

            if destination.exists():
                if not overwrite:
                    logger.warning(f"Destination directory already exists, skipping: {destination}")
                    return False
                else:
                    shutil.rmtree(destination)

            shutil.copytree(source, destination)
            logger.info(f"Copied directory from {source} to {destination}")
            return True

        except Exception as e:
            error_msg = f"Failed to copy directory from '{source}' to '{destination}': {e}"
            logger.error(error_msg)
            raise FileOperationError(error_msg)

    @staticmethod
    def file_exists(filepath: Union[str, Path]) -> bool:
        """
        Check if a file exists.

        Args:
            filepath: Path to check

        Returns:
            True if file exists, False otherwise
        """
        return Path(filepath).is_file()

    @staticmethod
    def directory_exists(dirpath: Union[str, Path]) -> bool:
        """
        Check if a directory exists.

        Args:
            dirpath: Path to check

        Returns:
            True if directory exists, False otherwise
        """
        return Path(dirpath).is_dir()
