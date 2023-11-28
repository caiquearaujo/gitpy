import git
from slugify import slugify;

from .. import gitop
from .. import terminal

class CommitCommand:
	def __init__(self, gitop: gitop.GitOp):
		self.git = gitop;

	def run(self):
		if (self.git.exists() == False):
			terminal.Terminal.err('Invalid command', 'Cannot find any repository on current working directory...');

		branch = self.git.currentBranch();
		terminal.Terminal.shouldContinue();

		type = terminal.Terminal.commitTypes();

		scope = slugify(terminal.Terminal.askInput('[*] Give a scope for your commit [<=20]', 20));
		title = terminal.Terminal.askInput('[*] Give a title for your commit [<=75]', 75);
		body = terminal.Terminal.askInput('Briefly describe your commit [<=180]', 180, False, jump=True);

		message = "{em} {tp}({sc}): {tt}\n\n{b}".format(em=type['emoji'],tp=type['type'],sc=scope,tt=title,b=body);

		terminal.Terminal.spacing();
		terminal.Terminal.printSuccess('Commit preview:\n');
		print(message+"\n");

		terminal.Terminal.shouldContinue();
		self.git.commit(message);

		_continue = terminal.Terminal.askYN('Do you want to push this commit to remote?');

		if ( _continue != False ):
			origin_name = None;
			keep_trying = True;

			while (keep_trying == True and origin_name == None):
				origin_name = terminal.Terminal.askInput('[*] Remote name', default = 'origin');

				if (self.git.remoteExists(origin_name) == False):
					terminal.Terminal.printErr('Invalid remote', 'Cannot find any remote with name: ' + origin_name);
					origin_name = None;
					keep_trying = terminal.Terminal.askYN('[*] Do you want to try a new remote name?');

			self.git.pushTo(branch, origin_name);
			terminal.Terminal.success('Commit finished and synchronized successfully...');

		terminal.Terminal.success('Commit finished successfully...');