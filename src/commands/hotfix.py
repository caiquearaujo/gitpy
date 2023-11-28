import git
from slugify import slugify;

from .. import gitop
from .. import terminal

class HotfixCommand:
	def __init__(self, gitop: gitop.GitOp):
		self.git = gitop;

	def run(self):
		if (self.git.exists() == False):
			terminal.Terminal.err('Invalid command', 'Cannot find any repository on current working directory...');

		option = terminal.Terminal.askChoices({
			1: { 'label': 'Create a new hotfix' },
			2: { 'label': 'Finish a hotfix' },
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

		if (branch != 'main'):
			terminal.Terminal.err('Invalid branch', 'You must be on "main" branch to create a new hotfix...');

		feat_name = slugify(terminal.Terminal.askInput('[*] What is the hotfix name?'));
		terminal.Terminal.warning('Your feature branch will be named as: hotfix/' + feat_name);
		terminal.Terminal.shouldContinue();

		track_branch = terminal.Terminal.askYN('[*] Do you want to track this branch on remote?');
		origin_name = None;

		while (track_branch == True and origin_name == None):
			origin_name = terminal.Terminal.askInput('[*] Remote name', default = 'origin');

			if (self.git.remoteExists(origin_name) == False):
				terminal.Terminal.printErr('Invalid remote', 'Cannot find any remote with name: ' + origin_name);
				origin_name = None;
				track_branch = terminal.Terminal.askYN('[*] Do you want to try a new remote name?');

		self.git.create('hotfix/' + feat_name, origin_name, track_branch);
		terminal.Terminal.success('New hotfix branch created successfully...');