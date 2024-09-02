from datetime import datetime;
from slugify import slugify;

from .. import gitop
from .. import terminal

class CreateHotfixCommand:
	def __init__(self, gitop: gitop.GitOp):
		self.git = gitop;

	def run(self):
		branch = self.git.currentBranch();

		if (branch != 'main'):
			terminal.Terminal.err('Invalid branch', 'You must be on "main" branch to create a new hotfix...');

		branch_name = datetime.now().strftime('%Y%m%d%H%M%S');

		terminal.Terminal.warning('Your hotfix branch will be named as: hotfix/' + branch_name);
		terminal.Terminal.shouldContinue();

		track_branch = terminal.Terminal.askYN('[*] Do you want to track this branch on remote?');
		origin_name = None;

		while (track_branch == True and origin_name == None):
			origin_name = terminal.Terminal.askInput('[*] Remote name', default = 'origin');

			if (self.git.remoteExists(origin_name) == False):
				terminal.Terminal.printErr('Invalid remote', 'Cannot find any remote with name: ' + origin_name);
				origin_name = None;
				track_branch = terminal.Terminal.askYN('[*] Do you want to try a new remote name?');

		self.git.create('hotfix/' + branch_name, origin_name, track_branch);
		terminal.Terminal.success('New hotfix branch created successfully...');

class FinishHotfixCommand:
	def __init__(self, gitop: gitop.GitOp):
		self.git = gitop;

	def run(self):
		branch = self.git.currentBranch();

		if ('hotfix/' not in branch):
			terminal.Terminal.err('Invalid branch', 'You must be on a hotfix branch to finish it...');

		untracked = self.git.hasUncommitedChanges();

		if (untracked):
			terminal.Terminal.warning('You have uncommited changes on this branch...');
			terminal.Terminal.err('Cannot finish', 'You must commit your changes before finish this hotfix...');

		self.git.checkout('main');
		self.git.merge('Merge branch "' + branch + '" into "main"');

		self.git.checkout('dev');
		self.git.merge('Merge branch "' + branch + '" into "dev"');

		keep_branch = terminal.Terminal.askYN('[*] Do you want to keep the hotfix branch?');

		if (keep_branch == False):
			self.git.delete(branch);

		terminal.Terminal.success('Hotfix branch merged successfully...');