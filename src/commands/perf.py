from datetime import datetime;
from slugify import slugify;

from .. import gitop
from .. import terminal

class CreatePerfCommand:
	def __init__(self, gitop: gitop.GitOp):
		self.git = gitop;

	def run(self):
		branch = self.git.currentBranch();

		if (branch != 'dev'):
			terminal.Terminal.err('Invalid branch', 'You must be on "dev" branch to create a new perf...');

		branch_name = datetime.now().strftime('%Y%m%d%H%M%S');

		terminal.Terminal.warning('Your perf branch will be named as: perf/' + branch_name);
		terminal.Terminal.shouldContinue();

		track_branch = terminal.Terminal.askYN('[*] Do you want to track this branch on remote?');
		origin_name = None;

		while (track_branch == True and origin_name == None):
			origin_name = terminal.Terminal.askInput('[*] Remote name', default = 'origin');

			if (self.git.remoteExists(origin_name) == False):
				terminal.Terminal.printErr('Invalid remote', 'Cannot find any remote with name: ' + origin_name);
				origin_name = None;
				track_branch = terminal.Terminal.askYN('[*] Do you want to try a new remote name?');

		self.git.create('perf/' + branch_name, origin_name, track_branch);
		terminal.Terminal.success('New perf branch created successfully...');

class FinishPerfCommand:
	def __init__(self, gitop: gitop.GitOp):
		self.git = gitop;

	def run(self):
		branch = self.git.currentBranch();

		if ('perf/' not in branch):
			terminal.Terminal.err('Invalid branch', 'You must be on a perf branch to finish it...');

		untracked = self.git.hasUncommitedChanges();

		if (untracked):
			terminal.Terminal.warning('You have uncommited changes on this branch...');
			terminal.Terminal.err('Cannot finish', 'You must commit your changes before finish this perf...');

		self.git.checkout('main');
		self.git.merge('Merge branch "' + branch + '" into "main"');

		self.git.checkout('dev');
		self.git.merge('Merge branch "' + branch + '" into "dev"');

		keep_branch = terminal.Terminal.askYN('[*] Do you want to keep the perf branch?');

		if (keep_branch == False):
			self.git.delete(branch);

		terminal.Terminal.success('Perf branch merged successfully...');