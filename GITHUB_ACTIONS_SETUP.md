# GitHub Actions Setup Instructions

Due to GitHub App permission restrictions, workflow files must be manually added to your repository. Follow these steps to set up the CI/CD system:

## 1. Create Workflow Files

Create the `.github/workflows/` directory and copy the workflow files:

### CI Workflow

```bash
mkdir -p .github/workflows
cp workflows-ci.yml .github/workflows/ci.yml
```

### Release Workflow

```bash
cp workflows-release.yml .github/workflows/release.yml
```

## 2. Configure PyPI Publishing (Optional)

To enable automated PyPI publishing:

1. Go to [PyPI's trusted publishers page](https://pypi.org/manage/account/publishing/)
2. Add a new trusted publisher with:
   - **PyPI Project Name**: `html22text`
   - **Owner**: `twardoch`
   - **Repository name**: `html22text`
   - **Workflow name**: `release.yml`
   - **Environment name**: `release`

## 3. Set Up GitHub Environment (Optional)

To protect releases:

1. In your GitHub repository, go to Settings → Environments
2. Create an environment named `release`
3. Add protection rules if needed

## 4. Test the Setup

### Test CI
1. Push changes to a feature branch
2. Create a pull request
3. CI runs automatically on push and PR events

### Test Release
1. Ensure you're on the main branch
2. Run the release script:
   ```bash
   ./scripts/release.sh v1.0.0
   ```
3. This creates a git tag and triggers the release workflow

## 5. Workflow Features

### CI Workflow (`ci.yml`)
- Runs on every push and pull request
- Tests on Ubuntu, Windows, macOS
- Tests Python versions 3.10, 3.11, 3.12
- Lints, type checks, and runs tests
- Uploads coverage reports
- Builds and validates packages

### Release Workflow (`release.yml`)
- Triggered by version tags (e.g., `v1.0.0`)
- Runs full test suite
- Builds packages
- Publishes to PyPI (if configured)
- Creates GitHub releases
- Builds executables for all platforms
- Attaches artifacts to releases

## 6. Manual Alternative

To publish manually:

1. Run the release workflow without the publish step
2. Download artifacts from GitHub releases
3. Upload to PyPI:
   ```bash
   ./scripts/build.sh
   twine upload dist/*
   ```

## 7. Repository Settings

Enable in your repository settings:
- **Actions**
- **Secrets and variables** (if using PyPI)
- **Environments** (if using release protection)

## 8. Troubleshooting

### Common Issues:
1. **Permission errors**: Verify GitHub App permissions
2. **PyPI errors**: Check trusted publisher settings
3. **Build failures**: Confirm dependencies in `pyproject.toml`
4. **Test failures**: Run `./scripts/test.sh` locally first

### Debug Steps:
1. Check the Actions tab for workflow status
2. Review logs for error messages
3. Test scripts locally before pushing
4. Verify git tags follow semantic versioning (`v1.2.3`)

## Next Steps

After setup:

1. Test with a small version bump
2. Monitor initial releases
3. Adjust configurations as needed
4. Add more platforms or Python versions if required

The CI/CD system will then handle:
- Automated testing and quality checks
- Multiplatform package builds
- PyPI publishing (if configured)
- GitHub releases with downloadable artifacts
- Pre-built executables for easier installation