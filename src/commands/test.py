import git
from slugify import slugify;

from .. import gitop
from .. import terminal

class TestCommand:
	def __init__(self, gitop: gitop.GitOp):
		self.git = gitop;

	def run(self):
		exists = self.git.remoteExists('origin');

		if (exists == False):
			terminal.Terminal.err('Invalid command', 'Cannot find any remote on current repository...');
		else:
			terminal.Terminal.success('Remote found successfully...');