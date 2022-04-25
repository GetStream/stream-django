const setupPyUpdater = {
    VERSION_REGEX: /version = "(.+)"/,

    readVersion: function (contents) {
        const version = this.VERSION_REGEX.exec(contents)[1];
        return version;
    },

    writeVersion: function (contents, version) {
        return contents.replace(this.VERSION_REGEX.exec(contents)[0], `version = "${version}"`);
    }
}

module.exports = {
    bumpFiles: [{ filename: './setup.py', updater: setupPyUpdater }],
}
