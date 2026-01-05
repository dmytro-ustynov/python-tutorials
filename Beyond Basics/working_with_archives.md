# Working with Archives in Python

## Why Archives Matter

Archives compress multiple files and directories into a single file for:
- **Distribution**: Send multiple files as one
- **Backup**: Compress and store data efficiently
- **Deployment**: Package applications and dependencies
- **Data transfer**: Reduce bandwidth usage

Common formats:
- `.zip` - Universal, built into most OS
- `.tar` - Unix/Linux standard (no compression)
- `.tar.gz` / `.tgz` - Compressed tar (gzip)
- `.tar.bz2` - Compressed tar (bzip2, better compression)
- `.tar.xz` - Compressed tar (xz, best compression)
- `.7z` - 7-Zip format (not built into Python)

## The zipfile Module

### Creating ZIP Archives

#### Basic Example

```python
import zipfile

# Create a new ZIP file
with zipfile.ZipFile('archive.zip', 'w') as zipf:
    # Add files
    zipf.write('document.txt')
    zipf.write('photo.jpg')
    zipf.write('data.csv')

print("Archive created!")
```

#### Compression Levels

```python
import zipfile

# No compression (fastest)
with zipfile.ZipFile('archive.zip', 'w', zipfile.ZIP_STORED) as zipf:
    zipf.write('largefile.txt')

# DEFLATE compression (most compatible, default)
with zipfile.ZipFile('archive.zip', 'w', zipfile.ZIP_DEFLATED) as zipf:
    zipf.write('largefile.txt')

# BZIP2 compression (better compression)
with zipfile.ZipFile('archive.zip', 'w', zipfile.ZIP_BZIP2) as zipf:
    zipf.write('largefile.txt')

# LZMA compression (best compression, Python 3.3+)
with zipfile.ZipFile('archive.zip', 'w', zipfile.ZIP_LZMA) as zipf:
    zipf.write('largefile.txt')
```

#### Compression Level Control

```python
import zipfile

with zipfile.ZipFile('archive.zip', 'w', zipfile.ZIP_DEFLATED, compresslevel=9) as zipf:
    # compresslevel: 0-9 (0=no compression, 9=max compression)
    zipf.write('data.txt')
```

#### Archiving Entire Directory

```python
import zipfile
import os

def zip_directory(directory_path, zip_path):
    """Archive entire directory preserving structure"""
    with zipfile.ZipFile(zip_path, 'w', zipfile.ZIP_DEFLATED) as zipf:
        # Walk through directory
        for root, dirs, files in os.walk(directory_path):
            for file in files:
                # Full path to file
                file_path = os.path.join(root, file)

                # Archive name (relative path)
                # This is CRITICAL for proper extraction!
                arcname = os.path.relpath(file_path, directory_path)

                zipf.write(file_path, arcname)

# Usage
zip_directory('my_project', 'my_project.zip')
```

**Why `arcname` matters**:
```python
# Wrong - stores absolute paths
zipf.write('/home/user/project/file.txt')
# In archive: /home/user/project/file.txt
# Extracts to: /home/user/project/file.txt (or fails!)

# Right - stores relative paths
zipf.write('/home/user/project/file.txt', 'project/file.txt')
# In archive: project/file.txt
# Extracts to: current_dir/project/file.txt
```

### Extracting ZIP Archives

#### Extract All Files

```python
import zipfile

with zipfile.ZipFile('archive.zip', 'r') as zipf:
    # Extract all files to current directory
    zipf.extractall()

    # Extract to specific directory
    zipf.extractall('extracted_files')
```

#### Extract Specific File

```python
import zipfile

with zipfile.ZipFile('archive.zip', 'r') as zipf:
    # Extract one file
    zipf.extract('document.txt', 'output_dir')
```

#### List Archive Contents

```python
import zipfile

with zipfile.ZipFile('archive.zip', 'r') as zipf:
    # List all files
    print("Files in archive:")
    for filename in zipf.namelist():
        print(f"  {filename}")

    # Detailed information
    print("\nDetailed info:")
    for info in zipf.infolist():
        print(f"{info.filename}")
        print(f"  Compressed size: {info.compress_size} bytes")
        print(f"  Uncompressed size: {info.file_size} bytes")
        print(f"  Compression ratio: {info.compress_size / info.file_size * 100:.1f}%")
```

#### Read File from Archive Without Extracting

```python
import zipfile

with zipfile.ZipFile('archive.zip', 'r') as zipf:
    # Read file as bytes
    with zipf.open('document.txt') as f:
        content = f.read()
        print(content.decode('utf-8'))

    # Or directly
    data = zipf.read('data.csv')
    print(data.decode('utf-8'))
```

### Adding to Existing Archive

```python
import zipfile

# Append mode
with zipfile.ZipFile('archive.zip', 'a') as zipf:
    zipf.write('newfile.txt')
```

## Critical Security Issue: Path Traversal Attack

### The Vulnerability

Malicious ZIP files can contain filenames with `../` to escape the extraction directory:

```python
# Malicious archive contains:
# ../../../etc/passwd
# ../../../../Windows/System32/evil.dll

# If you do this:
with zipfile.ZipFile('malicious.zip', 'r') as zipf:
    zipf.extractall()  # DANGER!

# Files are written OUTSIDE your intended directory!
# Could overwrite system files or plant malware
```

### Safe Extraction Function

```python
import zipfile
import os

def safe_extract(zip_path, extract_to):
    """Safely extract ZIP file, preventing path traversal attacks"""
    with zipfile.ZipFile(zip_path, 'r') as zipf:
        for member in zipf.namelist():
            # Normalize path
            member_path = os.path.normpath(member)

            # Check for path traversal
            if member_path.startswith('..') or os.path.isabs(member_path):
                raise Exception(f"Illegal file path in archive: {member}")

            # Extract
            zipf.extract(member, extract_to)

# Usage
try:
    safe_extract('untrusted.zip', 'safe_output')
    print("Extraction successful!")
except Exception as e:
    print(f"Security violation: {e}")
```

### Even Safer: Validate All Paths

```python
import zipfile
import os

def safe_extract_strict(zip_path, extract_to):
    """Ultra-safe extraction with path validation"""
    # Ensure extract_to is absolute
    extract_to = os.path.abspath(extract_to)

    with zipfile.ZipFile(zip_path, 'r') as zipf:
        for member in zipf.namelist():
            # Compute target path
            target_path = os.path.abspath(os.path.join(extract_to, member))

            # Ensure target is within extract_to directory
            if not target_path.startswith(extract_to + os.sep):
                raise Exception(f"Path traversal detected: {member}")

            # Extract
            zipf.extract(member, extract_to)

# Usage
safe_extract_strict('archive.zip', './output')
```

**Python 3.11.4+ has built-in protection**:
```python
# In Python 3.11.4+, this is safe by default
with zipfile.ZipFile('archive.zip', 'r') as zipf:
    zipf.extractall('output', filter='data')  # New filter parameter!

# filter options:
# 'data' - default, prevents most attacks
# 'fully_trusted' - no checks (use only for trusted sources)
# callable - custom validation function
```

### Educational Example: Creating a Test Archive with Path Traversal

**⚠️ CRITICAL WARNING ⚠️**

The following code demonstrates how to CREATE a malicious archive with path traversal paths. This is provided **STRICTLY FOR EDUCATIONAL PURPOSES ONLY**:
- To understand how these attacks work
- To test your own safe extraction functions
- For security research in controlled environments

**NEVER use this to create malicious archives for unauthorized purposes. Creating and distributing malicious archives is illegal and unethical. Use only in isolated test environments.**

#### Creating a Test Malicious Archive

```python
import zipfile
import os
import tempfile

def create_traversal_test_archive(output_path='test_traversal.zip'):
    """
    Create a test archive with path traversal attempts.

    ⚠️ FOR EDUCATIONAL/TESTING PURPOSES ONLY ⚠️
    Use this to test your safe extraction functions.
    """
    print("=" * 60)
    print("⚠️  CREATING TEST ARCHIVE WITH MALICIOUS PATHS")
    print("=" * 60)
    print("This archive is for TESTING safe extraction functions ONLY!")
    print()

    # Create temporary files with safe content
    with tempfile.TemporaryDirectory() as tmpdir:
        # Create a legitimate file
        safe_file = os.path.join(tmpdir, 'safe.txt')
        with open(safe_file, 'w') as f:
            f.write('This is a safe file.\n')

        # Create test content for malicious paths
        test_content = b'This is test content for security research.\n'

        with zipfile.ZipFile(output_path, 'w', zipfile.ZIP_DEFLATED) as zipf:
            # Add a normal file
            zipf.write(safe_file, 'safe.txt')
            print("✓ Added: safe.txt (legitimate file)")

            # Add files with traversal paths (using writestr to bypass OS checks)

            # Attempt to write to parent directory
            zipf.writestr('../escaped.txt', test_content)
            print("⚠️  Added: ../escaped.txt (parent directory escape)")

            # Attempt to write multiple levels up
            zipf.writestr('../../level2_escape.txt', test_content)
            print("⚠️  Added: ../../level2_escape.txt (2 levels up)")

            # Attempt to write to /etc (Unix)
            zipf.writestr('../../../etc/evil.conf', test_content)
            print("⚠️  Added: ../../../etc/evil.conf (system directory)")

            # Absolute path (Unix)
            zipf.writestr('/tmp/absolute_path.txt', test_content)
            print("⚠️  Added: /tmp/absolute_path.txt (absolute path)")

            # Windows path examples
            zipf.writestr('..\\..\\Windows\\System32\\evil.dll', test_content)
            print("⚠️  Added: ..\\..\\Windows\\System32\\evil.dll (Windows)")

            zipf.writestr('C:\\Windows\\evil.txt', test_content)
            print("⚠️  Added: C:\\Windows\\evil.txt (Windows absolute)")

            # Mixed separators
            zipf.writestr('../../../usr/local/../bin/test', test_content)
            print("⚠️  Added: ../../../usr/local/../bin/test (mixed)")

    print()
    print(f"✓ Created test archive: {output_path}")
    print("=" * 60)

    return output_path


def test_extraction_function(extraction_function, test_archive='test_traversal.zip'):
    """
    Test your safe extraction function against malicious archive.

    Args:
        extraction_function: Your safe_extract function to test
        test_archive: Path to test archive (created with create_traversal_test_archive)
    """
    print("\n" + "=" * 60)
    print("Testing extraction function")
    print("=" * 60)

    # Create temporary output directory
    with tempfile.TemporaryDirectory() as test_dir:
        print(f"Test extraction directory: {test_dir}")

        try:
            extraction_function(test_archive, test_dir)

            # Check what was extracted
            extracted_files = []
            for root, dirs, files in os.walk(test_dir):
                for file in files:
                    file_path = os.path.join(root, file)
                    rel_path = os.path.relpath(file_path, test_dir)
                    extracted_files.append(rel_path)

            print(f"\n✓ Extraction completed")
            print(f"✓ Files extracted: {len(extracted_files)}")
            print("\nExtracted files:")
            for f in extracted_files:
                print(f"  - {f}")

            # Check if any file escaped
            escaped = []
            for root, dirs, files in os.walk(os.path.dirname(test_dir)):
                for file in files:
                    file_path = os.path.join(root, file)
                    if not file_path.startswith(test_dir):
                        # Check if it's related to our test
                        if 'escaped' in file or 'evil' in file:
                            escaped.append(file_path)

            if escaped:
                print("\n❌ SECURITY BREACH: Files escaped the extraction directory!")
                for f in escaped:
                    print(f"  ❌ {f}")
                return False
            else:
                print("\n✅ SUCCESS: All path traversal attempts were blocked!")
                return True

        except Exception as e:
            print(f"\n✓ Extraction blocked with exception: {e}")
            print("✅ This is expected behavior for safe extraction functions!")
            return True


# Example usage for testing
if __name__ == "__main__":
    print("This script creates a TEST ARCHIVE with malicious paths")
    print("for SECURITY RESEARCH and TESTING purposes only.\n")

    # Create test archive
    test_archive = create_traversal_test_archive('test_malicious.zip')

    # Define a safe extraction function (example)
    def safe_extract_example(zip_path, extract_to):
        """Example safe extraction function"""
        extract_to = os.path.abspath(extract_to)

        with zipfile.ZipFile(zip_path, 'r') as zipf:
            for member in zipf.namelist():
                target_path = os.path.abspath(os.path.join(extract_to, member))

                if not target_path.startswith(extract_to + os.sep):
                    raise Exception(f"Path traversal detected: {member}")

            # If all checks pass, extract
            zipf.extractall(extract_to)

    # Test the safe extraction function
    test_extraction_function(safe_extract_example, test_archive)

    # Clean up
    if os.path.exists(test_archive):
        os.remove(test_archive)
        print(f"\n✓ Cleaned up test archive: {test_archive}")
```

#### What This Test Archive Demonstrates

The test archive contains several malicious path patterns:

1. **Relative parent traversal**: `../escaped.txt`
   - Attempts to write one directory above extraction point

2. **Multiple level traversal**: `../../level2_escape.txt`
   - Attempts to escape multiple directory levels

3. **System directory targeting**: `../../../etc/evil.conf`
   - Targets Unix system directories

4. **Absolute paths** (Unix): `/tmp/absolute_path.txt`
   - Uses absolute path instead of relative

5. **Windows paths**: `..\\..\\Windows\\System32\\evil.dll`
   - Windows-style directory traversal

6. **Windows absolute**: `C:\\Windows\\evil.txt`
   - Windows absolute path

7. **Mixed separators**: `../../../usr/local/../bin/test`
   - Combines traversal with confusing paths

#### Using This for Testing

This test archive is useful for:

1. **Testing your extraction functions**:
```python
# Test if your function catches all traversal attempts
create_traversal_test_archive('test.zip')
result = test_extraction_function(my_safe_extract_function, 'test.zip')
if result:
    print("Your extraction function is secure!")
```

2. **Educational demonstrations**:
```python
# Show students what unsafe extraction does
test_archive = create_traversal_test_archive('demo.zip')

print("\n❌ UNSAFE extraction (DO NOT DO THIS):")
with zipfile.ZipFile(test_archive, 'r') as zipf:
    print("Files that would be written:")
    for name in zipf.namelist():
        print(f"  {name}")
# DON'T actually extract!

print("\n✅ SAFE extraction:")
safe_extract_strict(test_archive, 'safe_output')
```

3. **Security audits**:
- Test extraction code in your applications
- Verify library behavior with malicious inputs
- Validate security controls

#### Important Notes

1. **The writestr() method** bypasses OS path validation, allowing creation of archives with any filename string, including traversal paths.

2. **Testing environment**: Always test in isolated environments (VMs, containers) to prevent accidental system compromise.

3. **Real-world malware**: Real malicious archives may use additional techniques:
   - Zip bombs (extreme compression ratios)
   - Symbolic link attacks
   - Special characters and encoding tricks
   - Extremely long filenames

4. **Cleanup**: Always clean up test archives after use:
```python
import os
if os.path.exists('test_malicious.zip'):
    os.remove('test_malicious.zip')
```

#### Testing Your Safe Extraction Code

Use the test archive to verify your extraction function:

```python
# Create test archive
test_zip = create_traversal_test_archive('security_test.zip')

# Test various extraction methods
print("\nTest 1: Unsafe extraction")
# Don't actually run this!
# zipfile.ZipFile(test_zip, 'r').extractall()  # WOULD BE DANGEROUS

print("\nTest 2: Safe extraction with validation")
try:
    safe_extract_strict(test_zip, 'test_output')
    print("✅ Extraction blocked malicious paths")
except Exception as e:
    print(f"✅ Caught: {e}")

print("\nTest 3: Python 3.11.4+ filter")
with zipfile.ZipFile(test_zip, 'r') as zipf:
    try:
        zipf.extractall('test_output', filter='data')
        print("✅ Built-in filter prevented traversal")
    except Exception as e:
        print(f"✅ Built-in protection: {e}")

# Cleanup
os.remove(test_zip)
```

**Remember**: This knowledge is for defense, not offense. Use it to protect your applications and educate others about security risks.

## Working with Relative Paths

### Why Relative Paths Matter

```python
# Project structure
my_project/
├── src/
│   ├── main.py
│   └── utils.py
├── data/
│   └── config.json
└── docs/
    └── README.md
```

**Goal**: Archive preserves this structure, extracts anywhere.

### Correct Approach

```python
import zipfile
import os

def create_project_archive(project_dir, output_zip):
    """Create archive with proper relative paths"""
    with zipfile.ZipFile(output_zip, 'w', zipfile.ZIP_DEFLATED) as zipf:
        # Get absolute path to project
        project_dir = os.path.abspath(project_dir)

        for root, dirs, files in os.walk(project_dir):
            for file in files:
                # Absolute path to file
                file_path = os.path.join(root, file)

                # Relative path from project_dir
                arcname = os.path.relpath(file_path, project_dir)

                # Add to archive
                zipf.write(file_path, arcname)

                print(f"Added: {arcname}")

# Create archive
create_project_archive('my_project', 'my_project.zip')
```

**Result** in archive:
```
src/main.py
src/utils.py
data/config.json
docs/README.md
```

### Including Parent Directory Name

```python
def create_project_archive_with_root(project_dir, output_zip):
    """Archive with project name as root directory"""
    project_name = os.path.basename(os.path.abspath(project_dir))

    with zipfile.ZipFile(output_zip, 'w', zipfile.ZIP_DEFLATED) as zipf:
        for root, dirs, files in os.walk(project_dir):
            for file in files:
                file_path = os.path.join(root, file)
                # Relative to project's parent, includes project name
                arcname = os.path.join(
                    project_name,
                    os.path.relpath(file_path, project_dir)
                )
                zipf.write(file_path, arcname)

# Create archive
create_project_archive_with_root('my_project', 'my_project.zip')
```

**Result**:
```
my_project/src/main.py
my_project/src/utils.py
my_project/data/config.json
my_project/docs/README.md
```

When extracted, creates `my_project/` directory automatically!

## The tarfile Module

TAR archives are common on Unix/Linux systems.

### Creating TAR Archives

```python
import tarfile

# Uncompressed TAR
with tarfile.open('archive.tar', 'w') as tar:
    tar.add('file.txt')
    tar.add('directory')

# GZIP compressed (.tar.gz)
with tarfile.open('archive.tar.gz', 'w:gz') as tar:
    tar.add('file.txt')

# BZIP2 compressed (.tar.bz2)
with tarfile.open('archive.tar.bz2', 'w:bz2') as tar:
    tar.add('file.txt')

# XZ compressed (.tar.xz)
with tarfile.open('archive.tar.xz', 'w:xz') as tar:
    tar.add('file.txt')
```

### Archive Directory with Relative Paths

```python
import tarfile
import os

def tar_directory(directory_path, tar_path):
    """Create TAR archive with relative paths"""
    with tarfile.open(tar_path, 'w:gz') as tar:
        # Add with arcname to use relative path
        tar.add(
            directory_path,
            arcname=os.path.basename(directory_path)
        )

# Usage
tar_directory('my_project', 'my_project.tar.gz')
```

### Extracting TAR Archives

```python
import tarfile

# Extract all
with tarfile.open('archive.tar.gz', 'r:gz') as tar:
    tar.extractall('output_dir')

# Extract specific file
with tarfile.open('archive.tar.gz', 'r:gz') as tar:
    tar.extract('specific_file.txt', 'output_dir')

# List contents
with tarfile.open('archive.tar.gz', 'r:gz') as tar:
    for member in tar.getmembers():
        print(f"{member.name} - {member.size} bytes")
```

### Safe TAR Extraction

TAR has the same path traversal vulnerability!

```python
import tarfile
import os

def safe_tar_extract(tar_path, extract_to):
    """Safely extract TAR archive"""
    extract_to = os.path.abspath(extract_to)

    with tarfile.open(tar_path, 'r:*') as tar:  # r:* auto-detects compression
        for member in tar.getmembers():
            # Compute target path
            target_path = os.path.abspath(os.path.join(extract_to, member.name))

            # Validate path
            if not target_path.startswith(extract_to + os.sep):
                raise Exception(f"Path traversal detected: {member.name}")

        # Extract all (already validated)
        tar.extractall(extract_to)

# Python 3.11.4+ safe by default
with tarfile.open('archive.tar.gz', 'r:gz') as tar:
    tar.extractall('output', filter='data')
```

## Practical Examples

### Example 1: Backup Script

```python
import zipfile
import os
from datetime import datetime

def backup_directory(source_dir, backup_dir):
    """Create timestamped backup of directory"""
    # Create backup filename with timestamp
    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
    source_name = os.path.basename(os.path.abspath(source_dir))
    backup_filename = f"{source_name}_backup_{timestamp}.zip"
    backup_path = os.path.join(backup_dir, backup_filename)

    # Create backup
    print(f"Creating backup: {backup_filename}")
    with zipfile.ZipFile(backup_path, 'w', zipfile.ZIP_DEFLATED) as zipf:
        for root, dirs, files in os.walk(source_dir):
            for file in files:
                file_path = os.path.join(root, file)
                arcname = os.path.relpath(file_path, source_dir)
                zipf.write(file_path, arcname)
                print(f"  Added: {arcname}")

    # Show results
    size_mb = os.path.getsize(backup_path) / (1024 * 1024)
    print(f"Backup complete: {backup_path} ({size_mb:.2f} MB)")

# Usage
backup_directory('/home/user/documents', '/home/user/backups')
```

### Example 2: Extract with Progress

```python
import zipfile
from tqdm import tqdm  # pip install tqdm

def extract_with_progress(zip_path, extract_to):
    """Extract ZIP with progress bar"""
    with zipfile.ZipFile(zip_path, 'r') as zipf:
        members = zipf.namelist()

        # Progress bar
        with tqdm(total=len(members), desc="Extracting") as pbar:
            for member in members:
                zipf.extract(member, extract_to)
                pbar.update(1)
                pbar.set_postfix_str(member)

# Usage
extract_with_progress('large_archive.zip', 'output')
```

### Example 3: Archive Filtering

```python
import zipfile
import os

def archive_python_files(source_dir, output_zip):
    """Archive only Python files, excluding __pycache__"""
    with zipfile.ZipFile(output_zip, 'w', zipfile.ZIP_DEFLATED) as zipf:
        for root, dirs, files in os.walk(source_dir):
            # Skip __pycache__ directories
            dirs[:] = [d for d in dirs if d != '__pycache__']

            for file in files:
                if file.endswith('.py'):
                    file_path = os.path.join(root, file)
                    arcname = os.path.relpath(file_path, source_dir)
                    zipf.write(file_path, arcname)
                    print(f"Added: {arcname}")

# Usage
archive_python_files('my_project', 'python_files.zip')
```

### Example 4: Compare Archive Contents

```python
import zipfile

def compare_archives(zip1_path, zip2_path):
    """Compare contents of two ZIP files"""
    with zipfile.ZipFile(zip1_path, 'r') as zip1:
        with zipfile.ZipFile(zip2_path, 'r') as zip2:
            files1 = set(zip1.namelist())
            files2 = set(zip2.namelist())

            # Files only in first archive
            only_in_1 = files1 - files2
            if only_in_1:
                print(f"Only in {zip1_path}:")
                for f in sorted(only_in_1):
                    print(f"  {f}")

            # Files only in second archive
            only_in_2 = files2 - files1
            if only_in_2:
                print(f"\nOnly in {zip2_path}:")
                for f in sorted(only_in_2):
                    print(f"  {f}")

            # Common files
            common = files1 & files2
            print(f"\nCommon files: {len(common)}")

# Usage
compare_archives('version1.zip', 'version2.zip')
```

### Example 5: Password-Protected Archive

```python
import zipfile

# Create password-protected archive
with zipfile.ZipFile('secure.zip', 'w', zipfile.ZIP_DEFLATED) as zipf:
    # Set password (must be bytes)
    zipf.setpassword(b'mysecretpassword')

    # Add files
    zipf.write('sensitive.txt')

# Extract password-protected archive
with zipfile.ZipFile('secure.zip', 'r') as zipf:
    # Provide password
    zipf.extractall(pwd=b'mysecretpassword')

# Or extract single file
with zipfile.ZipFile('secure.zip', 'r') as zipf:
    content = zipf.read('sensitive.txt', pwd=b'mysecretpassword')
    print(content.decode('utf-8'))
```

**Warning**: ZIP encryption is weak! For serious security, use separate encryption tools like GPG.

### Example 6: Memory-Efficient Processing

```python
import zipfile

def process_large_archive(zip_path):
    """Process large archive without extracting to disk"""
    with zipfile.ZipFile(zip_path, 'r') as zipf:
        for filename in zipf.namelist():
            if filename.endswith('.txt'):
                # Read file directly from archive
                with zipf.open(filename) as f:
                    # Process line by line (memory efficient)
                    for line in f:
                        text = line.decode('utf-8').strip()
                        # Process line
                        print(f"{filename}: {text[:50]}...")

# Usage
process_large_archive('logs.zip')
```

## Best Practices

### 1. Always Use Context Managers

```python
# Good
with zipfile.ZipFile('archive.zip', 'w') as zipf:
    zipf.write('file.txt')
# Automatically closes

# Bad
zipf = zipfile.ZipFile('archive.zip', 'w')
zipf.write('file.txt')
zipf.close()  # Might not be called if exception occurs
```

### 2. Use Relative Paths

```python
# Good
zipf.write('/home/user/project/file.txt', 'project/file.txt')

# Bad
zipf.write('/home/user/project/file.txt')  # Absolute path stored
```

### 3. Validate Untrusted Archives

```python
# Always validate before extracting untrusted archives
safe_extract_strict('untrusted.zip', 'output')
```

### 4. Choose Appropriate Compression

```python
# Text files: Use ZIP_DEFLATED or ZIP_LZMA
# Already compressed (images, videos): Use ZIP_STORED
# Maximum compression: Use tar.xz or ZIP_LZMA

# Example
with zipfile.ZipFile('docs.zip', 'w', zipfile.ZIP_DEFLATED) as zipf:
    zipf.write('document.txt')  # Compresses well

with zipfile.ZipFile('media.zip', 'w', zipfile.ZIP_STORED) as zipf:
    zipf.write('photo.jpg')  # Already compressed, don't waste time
```

### 5. Handle Errors Gracefully

```python
import zipfile

try:
    with zipfile.ZipFile('archive.zip', 'r') as zipf:
        zipf.extractall('output')
except zipfile.BadZipFile:
    print("Error: Corrupted ZIP file")
except FileNotFoundError:
    print("Error: ZIP file not found")
except PermissionError:
    print("Error: Permission denied")
```

### 6. Check Archive Integrity

```python
import zipfile

def verify_archive(zip_path):
    """Verify ZIP file integrity"""
    try:
        with zipfile.ZipFile(zip_path, 'r') as zipf:
            # Test all files
            result = zipf.testzip()
            if result is None:
                print("Archive is valid!")
                return True
            else:
                print(f"Corrupted file: {result}")
                return False
    except zipfile.BadZipFile:
        print("Invalid ZIP file")
        return False

# Usage
if verify_archive('important.zip'):
    # Safe to extract
    pass
```

## Advanced: Custom Compression

### Using shutil for High-Level Operations

```python
import shutil

# Create archive (auto-detects format from extension)
shutil.make_archive('output_name', 'zip', 'source_directory')

# Formats: 'zip', 'tar', 'gztar', 'bztar', 'xztar'
shutil.make_archive('backup', 'gztar', '/home/user/documents')

# Extract archive (auto-detects format)
shutil.unpack_archive('archive.zip', 'output_directory')
```

### Streaming Compression

```python
import zipfile
import io

# Create archive in memory
memory_file = io.BytesIO()

with zipfile.ZipFile(memory_file, 'w', zipfile.ZIP_DEFLATED) as zipf:
    zipf.writestr('file1.txt', 'Content of file 1')
    zipf.writestr('file2.txt', 'Content of file 2')

# Get bytes
zip_data = memory_file.getvalue()

# Save to file
with open('memory_archive.zip', 'wb') as f:
    f.write(zip_data)

# Or send over network, etc.
```

## Conclusion

Working with archives in Python:

1. **Use `zipfile` for ZIP**, `tarfile` for TAR
2. **Always use relative paths** with `arcname` parameter
3. **Validate paths** to prevent traversal attacks
4. **Choose appropriate compression** for file types
5. **Handle errors** and verify archive integrity
6. **Use context managers** for automatic cleanup

**Security Checklist**:
- [ ] Validate all paths before extraction
- [ ] Use Python 3.11.4+ filter parameter when available
- [ ] Never trust archives from untrusted sources
- [ ] Check file sizes before extraction (zip bombs)
- [ ] Verify archive integrity with `testzip()`

**Example: Complete Safe Archive Handler**:
```python
import zipfile
import os

class SafeArchive:
    def __init__(self, max_size_mb=100):
        self.max_size_mb = max_size_mb

    def create(self, source_dir, output_zip):
        """Create archive with relative paths"""
        with zipfile.ZipFile(output_zip, 'w', zipfile.ZIP_DEFLATED) as zipf:
            for root, dirs, files in os.walk(source_dir):
                for file in files:
                    file_path = os.path.join(root, file)
                    arcname = os.path.relpath(file_path, source_dir)
                    zipf.write(file_path, arcname)

    def extract(self, zip_path, extract_to):
        """Safely extract archive"""
        extract_to = os.path.abspath(extract_to)

        with zipfile.ZipFile(zip_path, 'r') as zipf:
            # Check total size
            total_size = sum(info.file_size for info in zipf.infolist())
            if total_size > self.max_size_mb * 1024 * 1024:
                raise Exception(f"Archive too large: {total_size / 1024 / 1024:.1f} MB")

            # Validate paths
            for member in zipf.namelist():
                target_path = os.path.abspath(os.path.join(extract_to, member))
                if not target_path.startswith(extract_to + os.sep):
                    raise Exception(f"Path traversal detected: {member}")

            # Extract
            zipf.extractall(extract_to)

# Usage
archive = SafeArchive(max_size_mb=500)
archive.create('my_project', 'project.zip')
archive.extract('project.zip', 'output')
```

Now you can safely and effectively work with archives in your Python projects!