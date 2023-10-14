#!/usr/bin/env sh

# File: install_ctakes.sh
# Author: xc383@drecel.edu
# Date: 2023-10-13
# Purpose: Script to install ctakes and add nessisary resources.

# REF: https://www.tutorialspoint.com/aborting-a-shell-script-on-any-command-fails#:~:text=If%20you%20want%20to%20make,use%20the%20set%20%2De%20option.
set -e

if [ -z $1 ]; then
	echo "Usage: install_ctakes.sh VERSION_NUMBER"
	exit 1
fi

# Set up install variables
VERSION_NUMBER=$1
TMP_DIR=tmp_ctakes
CTAKES_HOME="apache-ctakes-$VERSION_NUMBER"
CTAKES_ZIP_FILE="apache-ctakes-$VERSION_NUMBER-bin.tar.gz"
CTAKES_URL="https://dlcdn.apache.org//ctakes/ctakes-$VERSION_NUMBER/$CTAKES_ZIP_FILE"
RESOURCES_ZIP_FILE="ctakes-resources-4.0-bin.zip"
RESOURCES_URL="http://sourceforge.net/projects/ctakesresources/files/ctakes-resources-4.0-bin.zip"

echo "[!] Installing cTakes v$VERSION_NUMBER"

# download ctakes
wget $CTAKES_URL
tar -xvzf $CTAKES_ZIP_FILE

# download resources
mkdir $TMP_DIR
wget $RESOURCES_URL -P $TMP_DIR/
unzip $TMP_DIR/$RESOURCES_ZIP_FILE -d $TMP_DIR
cp -R $TMP_DIR/resources/* $CTAKES_HOME/resources

# Clean up
rm $CTAKES_ZIP_FILE
rm -r $TMP_DIR

# Print details
echo "Documentation: https://cwiki.apache.org/confluence/collector/pages.action?key=CTAKES"
echo "Run Clinical Pipeline:"
echo "Usage: ./apache-ctakes-$VERSION_NUMBER/bin/runClinicalPipeline.sh -i \$IN_DIRECTORY --xmiOut \$OUT_DIRECTORY --key $UMLS_KEY --user \$UMLS_USER --pass \$UMLS_PASS"

