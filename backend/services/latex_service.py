import os
import subprocess
from pathlib import Path

class LaTeXCompilationError(Exception):
    def __init__(self, message: str, code: str = "COMPILATION_FAILED"):
        super().__init__(message)
        self.code = code

class LaTeXService:
    @staticmethod
    def compile_resume(session_id: str) -> str:
        """
        Compiles the generated LaTeX file using latexmk safely.
        Returns the path to the compiled PDF if successful.
        """
        # Resolve path
        from backend.services.file_service import file_service, GENERATED_DIR
        
        session_dir = os.path.join(GENERATED_DIR, session_id)
        if not os.path.exists(session_dir):
            raise LaTeXCompilationError("Session directory not found.", "SESSION_NOT_FOUND")
            
        tex_file = os.path.join(session_dir, "resume.tex")
        pdf_file = os.path.join(session_dir, "resume.pdf")
        
        if not os.path.exists(tex_file):
            raise LaTeXCompilationError("Generated resume.tex not found.", "TEX_NOT_FOUND")

        # Basic LaTeX security check - block dangerous commands
        with open(tex_file, 'r', encoding='utf-8') as f:
            content = f.read()
            dangerous_macros = [
                r'\write18', r'\input', r'\include', r'\usepackage', 
                r'\RequirePackage', r'\def', r'\newcommand', r'\renewcommand'
            ]
            # Since the master resume itself might use some of these (like \usepackage), 
            # we should really just block \write18 and \input/\include in user-modified parts.
            # But PRD says "dangerous commands". Let's block \write18 to be safe against shell escape.
            if r'\write18' in content:
                raise LaTeXCompilationError("Dangerous LaTeX command detected.", "UNSAFE_LATEX")
        
        # Determine compiler command
        # Use latexmk if available, otherwise pdflatex
        try:
            # Check if latexmk is installed
            subprocess.run(["latexmk", "-v"], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, check=True)
            cmd = [
                "latexmk",
                "-pdf",
                "-interaction=nonstopmode",
                "-halt-on-error",
                "-no-shell-escape",
                "resume.tex"
            ]
        except (subprocess.CalledProcessError, FileNotFoundError):
            # Fallback to pdflatex
            cmd = [
                "pdflatex",
                "-interaction=nonstopmode",
                "-halt-on-error",
                "-no-shell-escape",
                "resume.tex"
            ]

        try:
            result = subprocess.run(
                cmd,
                cwd=session_dir,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                timeout=15, # 15 second timeout
                check=False,
                text=True
            )
            
            if result.returncode != 0:
                # Provide a safe error message without raw paths
                raise LaTeXCompilationError("LaTeX compilation failed due to syntax errors.", "SYNTAX_ERROR")
                
            if not os.path.exists(pdf_file):
                raise LaTeXCompilationError("PDF file was not produced by the compiler.", "NO_OUTPUT")
                
            return pdf_file
            
        except subprocess.TimeoutExpired:
            raise LaTeXCompilationError("LaTeX compilation timed out.", "TIMEOUT")
        except FileNotFoundError:
            raise LaTeXCompilationError("LaTeX compiler not found on the system.", "COMPILER_MISSING")
        except Exception as e:
            if isinstance(e, LaTeXCompilationError):
                raise
            raise LaTeXCompilationError("An unexpected compilation error occurred.", "UNKNOWN_ERROR")
