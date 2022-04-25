/*
Here we're trying to parse the latest changes from CHANGELOG.md file.
The changelog looks like this:

## 0.0.3
- Something #3
## 0.0.2
- Something #2
## 0.0.1
- Something #1

In this case we're trying to extract "- Something #3" since that's the latest change.
*/
module.exports = () => {
	const fs = require('fs');

	changelog = fs.readFileSync('CHANGELOG.md', 'utf8');
	releases = changelog.match(/## [?[0-9](.+)/g);

	current_release = changelog.indexOf(releases[0]);
	previous_release = changelog.indexOf(releases[1]);

	latest_changes = changelog.substr(current_release, previous_release - current_release);

	return latest_changes;
};
