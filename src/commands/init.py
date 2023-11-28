import git

from .. import gitop
from .. import terminal

class InitCommand:
	def __init__(self, gitop: gitop.GitOp):
		self.git = gitop;

	def run(self):
		if (self.git.exists() != False):
			terminal.Terminal.err('Invalid command', 'The repository has already been started in the current working directory...');

		self.git.init();

		self.git.commit(':tada: initial(repo): First commit');
		self.git.renameTo('main');

		add_origin = terminal.Terminal.askYN('[*] Do you want to add a remote origin?');
		origin_name = None;
		origin_url = None;

		if (add_origin == True):
			origin_name = terminal.Terminal.askInput('[*] What is the remote name?', default = 'origin');
			origin_url = terminal.Terminal.askInput('[*] What is the remote URL?');

			self.git.remote(origin_url, origin_name);
			self.git.pushTo('main');

		self.git.create('dev', origin_name, add_origin);
		terminal.Terminal.success('Repository initialized successfully...');