import subprocess
import os

def test_memory_leak():
    # 1. Compile the C++ file with AddressSanitizer
    compile_process = subprocess.run(
        ["clang++", "-fsanitize=address", "-g", "jenkins/jenkins.cpp", "jenkins/buggy.cpp", "-o", "buggy"],
        capture_output=True,
        text=True
    )
    assert compile_process.returncode == 0, f"Compilation failed: {compile_process.stderr}"

    # 2. Force LeakSanitizer ON in the environment variables for the CI pipeline
    asan_env = os.environ.copy()
    asan_env["ASAN_OPTIONS"] = "detect_leaks=1"

    # 3. Run the compiled binary with the custom environment
    run_process = subprocess.run(
        ["./buggy"],
        capture_output=True,
        text=True,
        env=asan_env
    )

    # 4. Check the outputs
    error_output = run_process.stderr
    
    # ASan will exit with a non-zero code if it finds a leak
    assert run_process.returncode != 0, "Expected non-zero exit code due to memory leak!"
    assert "AddressSanitizer" in error_output or "leak" in error_output.lower(), \
        f"Expected AddressSanitizer to catch a memory leak. Stderr was: {error_output}"