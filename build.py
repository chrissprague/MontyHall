#!/usr/bin/env python3
"""
Build script for the project.
Handles compilation of protobuf files and other build tasks.
"""
import os
import subprocess
import sys

def check_protoc():
    """Check if protoc is installed."""
    try:
        subprocess.run(['protoc', '--version'], capture_output=True, check=True)
    except (subprocess.CalledProcessError, FileNotFoundError):
        print("Error: protoc (Protocol Buffers compiler) is not installed.")
        print("Please install it using:")
        print("  sudo apt-get install -y protobuf-compiler  # For Ubuntu/Debian")
        print("  brew install protobuf                     # For macOS")
        print("  choco install protobuf                    # For Windows")
        sys.exit(1)

def compile_protos():
    """Compile all .proto files in the src directory."""
    proto_files = [f for f in os.listdir('src') if f.endswith('.proto')]
    if not proto_files:
        print("No .proto files found in src directory")
        return

    for proto_file in proto_files:
        print(f"Compiling {proto_file}...")
        try:
            subprocess.run([
                'protoc',
                f'--python_out=.',
                f'src/{proto_file}'
            ], check=True)
            print(f"Successfully compiled {proto_file}")
        except subprocess.CalledProcessError as e:
            print(f"Error compiling {proto_file}: {e}")
            sys.exit(1)

def main():
    """Main build function."""
    print("Starting build process...")
    
    # Check for protoc
    check_protoc()
    
    # Compile protos
    compile_protos()
    
    print("Build completed successfully!")

if __name__ == '__main__':
    main() 