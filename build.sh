#!/bin/bash
set -e   # Exit immediately on any error

echo "============================================"
echo "  Bookshelf API - CI Build Script"
echo "============================================"

# ── Step 1: Install dependencies ──────────────────────────────────────────────
echo ""
echo "[1/4] Installing dependencies..."
pip install -r requirements.txt --quiet

# ── Step 2: Run tests with coverage ───────────────────────────────────────────
echo ""
echo "[2/4] Running test suite..."
pytest tests/ -v --tb=short --cov=app --cov-report=term-missing

# ── Step 3: Package the application ───────────────────────────────────────────
echo ""
echo "[3/4] Packaging application..."
BUILD_ID=${BUILD_NUMBER:-0}
ARTIFACT_NAME="bookshelf-api-build-${BUILD_ID}.zip"

zip -r "${ARTIFACT_NAME}" app/ requirements.txt

echo "  Artifact created: ${ARTIFACT_NAME}"

# ── Step 4: Verify artifact ────────────────────────────────────────────────────
echo ""
echo "[4/4] Verifying artifact..."
if [ -f "${ARTIFACT_NAME}" ]; then
    SIZE=$(du -sh "${ARTIFACT_NAME}" | cut -f1)
    echo "  SUCCESS: ${ARTIFACT_NAME} (${SIZE})"
    echo "  Contents:"
    unzip -l "${ARTIFACT_NAME}"
else
    echo "  FAILURE: Artifact not found!"
    exit 1
fi

echo ""
echo "============================================"
echo "  Build PASSED. Artifact ready for deploy."
echo "============================================"
