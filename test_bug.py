import subprocess

def test_memory_leak():
    # Compile the C++ file with AddressSanitizer
    compile_process = subprocess.run(
        ["clang++", "-fsanitize=address", "-g", "jenkins/jenkins.cpp", "-o", "buggy"],
        capture_output=True,
        text=True
    )
    assert compile_process.returncode == 0, f"Compilation failed: {compile_process.stderr}"

    # Run the compiled binary
    run_process = subprocess.run(
        ["./buggy"],
        capture_output=True,
        text=True
    )

    # AddressSanitizer outputs leak details to stderr and exits with a non-zero code
    error_output = run_process.stderr
    assert "AddressSanitizer" in error_output or "leak" in error_output.lower(), \
        "Expected AddressSanitizer to catch a memory leak, but clean run detected."