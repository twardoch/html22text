# GitHub Actions Setup Instructions

Due to GitHub App permission restrictions, the workflow files need to be manually added to your repository. Here's how to set up the complete CI/CD system:

## 1. Create Workflow Files

Create the `.github/workflows/` directory and add the following files:

### Create CI Workflow

```bash
mkdir -p .github/workflows
cp workflows-ci.yml .github/workflows/ci.yml
```

### Create Release Workflow

```bash
cp workflows-release.yml .github/workflows/release.yml
```

## 2. Configure PyPI Publishing (Optional)

For automated PyPI publishing, you'll need to configure trusted publishing:

1. Go to [PyPI](https://pypi.org/manage/account/publishing/)
2. Add a new trusted publisher with:
   - **PyPI Project Name**: `html22text`
   - **Owner**: `twardoch`
   - **Repository name**: `html22text`
   - **Workflow name**: `release.yml`
   - **Environment name**: `release`

## 3. Set Up GitHub Environment (Optional)

For release protection:

1. Go to your GitHub repository settings
2. Navigate to "Environments"
3. Create a new environment named `release`
4. Add protection rules if desired

## 4. Test the Setup

### Test CI
1. Push changes to a feature branch
2. Create a pull request
3. CI should run automatically

### Test Release
1. Ensure you're on the main branch
2. Run the release script:
   ```bash
   ./scripts/release.sh v1.0.0
   ```
3. This will create a git tag and trigger the release workflow

## 5. Workflow Features

### CI Workflow (`ci.yml`)
- Runs on every push and pull request
- Tests across multiple platforms (Ubuntu, Windows, macOS)
- Tests across Python versions (3.10, 3.11, 3.12)
- Performs linting, type checking, and testing
- Uploads coverage reports
- Builds and validates packages

### Release Workflow (`release.yml`)
- Triggered by version tags (v1.0.0, v1.2.3, etc.)
- Runs full test suite
- Builds packages
- Publishes to PyPI (if configured)
- Creates GitHub releases
- Builds executables for all platforms
- Attaches artifacts to releases

## 6. Manual Alternative

If you prefer not to use automated PyPI publishing, you can:

1. Use the release workflow without the publish step
2. Download artifacts from GitHub releases
3. Manually upload to PyPI using:
   ```bash
   ./scripts/build.sh
   twine upload dist/*
   ```

## 7. Repository Settings

Ensure your repository has:
- **Actions** enabled
- **Secrets and variables** configured (if using PyPI)
- **Environments** set up (if using release protection)

## 8. Troubleshooting

### Common Issues:

1. **Permission errors**: Ensure the GitHub App has proper permissions
2. **PyPI errors**: Check trusted publisher configuration
3. **Build failures**: Verify dependencies in `pyproject.toml`
4. **Test failures**: Run `./scripts/test.sh` locally first

### Debug Steps:

1. Check the Actions tab in your GitHub repository
2. Review workflow logs for errors
3. Test scripts locally before pushing
4. Verify git tags are properly formatted (v1.2.3)

## Next Steps

After setting up the workflows:

1. Test with a small version bump
2. Monitor the first few releases
3. Adjust configurations as needed
4. Add more platforms or Python versions if required

The complete CI/CD system will then provide:
- Automated testing and quality checks
- Multiplatform releases
- PyPI publishing
- GitHub releases with downloadable artifacts
- Pre-built executables for easy installation