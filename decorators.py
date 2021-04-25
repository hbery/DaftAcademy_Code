from functools import wraps

def greetings(wrapped_func):
	
	def wrapper(*args, **kwargs):
		new_string = ' '.join([name.capitalize() for name in wrapped_func(*args, **kwargs).split(' ')])
		return f'Hello {new_string}'
	
	return wrapper

def is_palindrome(wrapped_func):
	
	def wrapper(*args, **kwargs):
		string = wrapped_func(*args, **kwargs)
		clean_string = ''.join([character.lower() for character in string if character.isalnum()])

		if clean_string == clean_string[::-1]:
			return f'{string} - is palindrome'
		else:
			return f'{string} - is not palindrome'

	return wrapper

def format_output(*keys):

	def decorator(wrapped_func):
		def wrapper(*args, **kwargs):
			wrapped_dict = wrapped_func(*args, **kwargs)
			wd_keys = wrapped_dict.keys()

			new_dict = {}
			for key in keys:
				if key not in wrapped_dict.keys():
					if '__' not in key:
						raise ValueError
					else:
						multiple_keys = key.split('__')
						for mkey in multiple_keys:
							if mkey not in wd_keys:
								raise ValueError
						new_dict[key] = ' '.join([wrapped_dict[mkey] for mkey in multiple_keys])
				else:
					new_dict[key] = wrapped_dict[key]

			return new_dict
		return wrapper
	return decorator

def add_instance_method(class_def):
	def decorator(wrapped_func):
		@wraps(wrapped_func)
		def wrapper(self, *args, **kwargs):
			return wrapped_func(*args, **kwargs)
		setattr(class_def, wrapped_func.__name__, wrapper)
		return wrapped_func
	return decorator

def add_class_method(class_def):
	def decorator(wrapped_func):			
		setattr(class_def, wrapped_func.__name__, wrapped_func)
		return wrapped_func
	return decorator