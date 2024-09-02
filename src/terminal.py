import colorama;
import sys;

class Terminal:

	@staticmethod
	def askChoices (choices, abort_option = -1):
		option = 0;
		print();

		while (option <= 0):
			for key in choices.keys():
				print(colorama.Fore.YELLOW, '[', key, ']', colorama.Fore.RESET ,'\t', choices[key]['label']);

			try:
				print();
				option = int(input('[*] Set an option' + colorama.Fore.GREEN + ' > ' + colorama.Fore.RESET));
			except:
				option = 0;

		if ( option == abort_option ):
			Terminal.success('Operation aborted successfully.');

		return option;

	@staticmethod
	def commitTypes ():
		commit_types = {
			1: { 'emoji': ':sparkles:', 'preview': '✨', 'type': 'feat', 'txt': "Features" },
			2: { 'emoji': ':bug:', 'preview': '🐛', 'type': 'fix', 'txt': "Bug Fixes" },
			3: { 'emoji': ':books:', 'preview': '📚', 'type': 'docs', 'txt': "Documentation" },
			4: { 'emoji': ':gem:', 'preview': '💎', 'type': 'style', 'txt': "Styles" },
			5: { 'emoji': ':package:', 'preview': '📦', 'type': 'refactor', 'txt': "Code Refactoring" },
			6: { 'emoji': ':racehorse:', 'preview': '🐎', 'type': 'perf', 'txt': "Performance Improvements" },
			7: { 'emoji': ':rotating_light:', 'preview': '🚨', 'type': 'test', 'txt': "Tests" },
			8: { 'emoji': ':wrench:', 'preview': '🔧', 'type': 'build', 'txt': "Builds" },
			9: { 'emoji': ':gear:', 'preview': '⚙️', 'type': 'ci', 'txt': "Continuous Integrations" },
			10: { 'emoji': ':recycle:', 'preview': '♻️', 'type': 'chore', 'txt': "Chores" },
			11: { 'emoji': ':rewind:', 'preview': '⏪', 'type': 'revert', 'txt': "Reverts" },
			12: { 'emoji': ':arrow_double_up:', 'preview': '⏫', 'type': 'dependencies', 'txt': "Dependencies" },
			13: { 'emoji': ':arrow_double_up:', 'preview': '⏫', 'type': 'peerDependencies', 'txt': "Peer dependencies" },
			14: { 'emoji': ':arrow_double_up:', 'preview': '⏫', 'type': 'devDependencies', 'txt': "Dev dependencies" },
			15: { 'emoji': ':card_index:', 'preview': '📇', 'type': 'metadata', 'txt': "Metadata" },
			16: { 'emoji': ':bookmark:', 'preview': '🔖', 'type': 'version', 'txt': "Version tag" },
			17: { 'emoji': ':lock:', 'preview': '🔒', 'type': 'security', 'txt': "Security" },
			18: { 'emoji': ':pencil:', 'preview': '✏️', 'type': 'text', 'txt': "Text" },
			19: { 'emoji': ':ambulance:', 'preview': '🚑', 'type': 'critical', 'txt': "Critical changes" },
			20: { 'emoji': ':ok_hand:', 'preview': '👌', 'type': 'review', 'txt': "Code review" },
			21: { 'emoji': ':recycle:', 'preview': '♻️', 'type': 'review', 'txt': "Content review" },
			22: { 'emoji': ':bricks:', 'preview': '🧱', 'type': 'other', 'txt': "Other" },
			23: { 'emoji': '', 'preview': '', 'type': 'abort', 'txt': "Abort commit" },
		}

		type = 0;

		print();

		while (type <= 0):
			for key in commit_types.keys():
				print(colorama.Fore.YELLOW, '[', key, ']', colorama.Fore.RESET ,'\t', commit_types[key]['preview'], commit_types[key]['txt']);

			try:
				print();
				type = int(input('[*] Set the commit type' + colorama.Fore.GREEN + ' > ' + colorama.Fore.RESET));
			except:
				type = 0;

		if ( type == 23 ):
			Terminal.success('Commit aborted successfully.');

		return commit_types[type];

	@staticmethod
	def askInput (question: str, max: int = -1, required: bool = True, default: str = None, jump: bool = False):
		while True:
			message = question + colorama.Fore.GREEN + ' > ' + colorama.Fore.RESET;

			if ( default ):
				message += colorama.Fore.YELLOW + ' [' + default + ']' + colorama.Fore.RESET;

			if (jump):
				message += "\n";

			response = input(message);

			if ( max < 0 ):
				max = len(response);

			if ( required ) :
				if ( len(response) == 0 and default != None ):
					return default;

				if ( len(response) != 0 and len(response) <= max ):
					return response;

				Terminal.printErr('Unexpected value', 'You need to set an answer...');

				if (len(response) > max):
					Terminal.printErr('Unexpected value', 'Maximum of {m} character(s) limit reached...\n'.format(m=max));
			else:
				if ( default != None ):
					return default;

				return response or "";

	@staticmethod
	def askYN (question: str, default: str = 'yes'):
		valid = {"yes": True, "y": True, "no": False, "n": False};

		if default is None:
			prompt = " [y/n] ";
		elif default == "yes":
			prompt = " [Y/n] ";
		elif default == "no":
			prompt = " [y/N] ";
		else:
			default = 'yes';
			prompt = " [Y/n] ";

		while True:
			choice = input(question + prompt + colorama.Fore.GREEN + '> ' + colorama.Fore.RESET).lower();

			if default is not None and choice == "":
				return valid[default];
			elif choice in valid:
				return valid[choice];
			else:
				Terminal.printErr('Unexpected value', 'Please, ask with: `y`, `n`, `yes` ou `no`.');

	@staticmethod
	def shouldContinue():
		_continue = Terminal.askYN('Do you want to continue?');

		if ( _continue == False ):
			Terminal.success('Operation aborted successfully...');

	@staticmethod
	def err (err = 'Erro', message = 'Something went wrong'):
		Terminal.printErr(err, message);
		sys.exit(2);

	@staticmethod
	def success (message = 'Everything is fine...'):
		Terminal.printSuccess(message);
		sys.exit();

	@staticmethod
	def warning (message = 'Everything is fine...'):
		Terminal.printWarning(message);

	@staticmethod
	def spacing ():
		print("\n");

	@staticmethod
	def printErr (err = 'Erro', message = 'Something went wrong'):
		print(
			colorama.Back.RED
			+ err + ' >'
			+ colorama.Back.RESET
			+ colorama.Fore.RED
			+ ' ' + message
			+ colorama.Fore.RESET
		);

	@staticmethod
	def printSuccess (message = 'Something went wrong'):
		print(colorama.Fore.GREEN + message + colorama.Fore.RESET);

	@staticmethod
	def printWarning (message = 'Something went wrong'):
		print(colorama.Fore.YELLOW + message + colorama.Fore.RESET);
