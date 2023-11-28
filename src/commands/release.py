import git
from slugify import slugify;

from .. import gitop
from .. import terminal

class ReleaseCommand:
	def __init__(self, gitop: gitop.GitOp):
		self.git = gitop;

	def run(self):
		if (self.git.exists() == False):
			terminal.Terminal.err('Invalid command', 'Cannot find any repository on current working directory...');

		option = terminal.Terminal.askChoices({
			1: { 'label': 'Create a new release' },
			2: { 'label': 'Finish a release' },
			3: { 'label': 'Abort' },
		}, 3)

		switcher = {
			1: lambda : self.create(),
			2: lambda : self.finish(),
		}

		func = switcher.get(option, False);
		func();

	def create(self):
		if (self.git.exists() == False):
			terminal.Terminal.err('Invalid command', 'Cannot find any repository on current working directory...');

		branch = self.git.currentBranch();

		if (branch != 'dev'):
			terminal.Terminal.err('Invalid branch', 'You must be on "dev" branch to create a new release...');

		feat_name = slugify(terminal.Terminal.askInput('[*] What is the release version? (e.g. 1.0.0)'));
		terminal.Terminal.warning('Your release branch will be named as: release/' + feat_name);
		terminal.Terminal.shouldContinue();

		track_branch = terminal.Terminal.askYN('[*] Do you want to track this branch on remote?');
		origin_name = None;

		while (track_branch == True and origin_name == None):
			origin_name = terminal.Terminal.askInput('[*] Remote name', default = 'origin');

			if (self.git.remoteExists(origin_name) == False):
				terminal.Terminal.printErr('Invalid remote', 'Cannot find any remote with name: ' + origin_name);
				origin_name = None;
				track_branch = terminal.Terminal.askYN('[*] Do you want to try a new remote name?');

		self.git.create('release/' + feat_name, origin_name, track_branch);
		terminal.Terminal.success('New release branch created successfully...');