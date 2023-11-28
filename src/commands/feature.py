import argparse
import git
from slugify import slugify;

from .. import gitop
from .. import terminal

class FeatureCommand:
	def __init__(self, gitop: gitop.GitOp):
		self.git = gitop;

	def run(self):
		if (self.git.exists() == False):
			terminal.Terminal.err('Invalid command', 'Cannot find any repository on current working directory...');

		option = terminal.Terminal.askChoices({
			1: { 'label': 'Create a new feature' },
			2: { 'label': 'Finish a feature' },
			3: { 'label': 'Abort' },
		}, 3)

		switcher = {
			1: lambda : self.create(),
			2: lambda : self.finish(),
		}

		func = switcher.get(option, False);
		func();

	def create(self):
		branch = self.git.currentBranch();

		if (branch != 'dev'):
			terminal.Terminal.err('Invalid branch', 'You must be on "dev" branch to create a new feature...');

		feat_name = slugify(terminal.Terminal.askInput('[*] What is the feature name?'));
		terminal.Terminal.warning('Your feature branch will be named as: feature/' + feat_name);
		terminal.Terminal.shouldContinue();

		track_branch = terminal.Terminal.askYN('[*] Do you want to track this branch on remote?');
		origin_name = None;

		while (track_branch == True and origin_name == None):
			origin_name = terminal.Terminal.askInput('[*] Remote name', default = 'origin');

			if (self.git.remoteExists(origin_name) == False):
				terminal.Terminal.printErr('Invalid remote', 'Cannot find any remote with name: ' + origin_name);
				origin_name = None;
				track_branch = terminal.Terminal.askYN('[*] Do you want to try a new remote name?');

		self.git.create('feature/' + feat_name, origin_name, track_branch);
		terminal.Terminal.success('New feature branch created successfully...');

	def finish(self):
		branch = self.git.currentBranch();

		if ('feature/' not in branch):
			terminal.Terminal.err('Invalid branch', 'You must be on a feature branch to finish it...');

		untracked = self.git.hasUncommitedChanges();

		if (untracked):
			terminal.Terminal.warning('You have uncommited changes on this branch...');
			terminal.Terminal.err('Cannot finish', 'You must commit your changes before finish this feature...');

		self.git.checkout('dev');
		self.git.merge('Merge branch "' + branch + '" into "dev"');

		keep_branch = terminal.Terminal.askYN('[*] Do you want to keep the feature branch?');

		if (keep_branch == False):
			self.git.delete(branch);

		terminal.Terminal.success('Feature branch merged successfully...');