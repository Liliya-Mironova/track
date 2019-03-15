import time
import random


def timer (function):
	print ("timer")
	def wrapper (*args, **kwargs):
		print("timer.wrapper")
		print(args, kwargs)
		start_ts = time.time()
		result = function(*args, **kwargs)
		end_ts = time.time()
		print("Time of execution of function {} is {} ms.".format(function.__name__, (end_ts-start_ts) * 1000))
		return result
	return wrapper

def sleeper (from_, to_): # для передачи аргументов
	print("sleeper")
	def sleeper_(function):
		print("sleeper_")
		def wrapper(*args, **kwargs):
			print("wrapper")
			time_to_sleep = random.randint(from_, to_)
			print("We gonna sleep {} seconds".format(time_to_sleep))
			time.sleep(random.randint(from_, to_))
			result = function(*args, **kwargs)
			return result
		return wrapper
	return sleeper_

@sleeper(1, 3) # the order is important, the next executes the 1st
@timer
def foo(a,b):
	print("foo")
	# time.sleep(5)
	return a + b

if __name__ == "__main__":
	print(foo(b=10, a=5)) # 15
	# () {'b': 10, 'a': 5}
	# Time of execution of function foo is 5001.487731933594 ms.
	# 15

	# () {'b': 10, 'a': 5}
	# Time of execution of function wrapper is 3003.237247467041 ms.
	# 15

	# We gonna sleep 2 seconds
	# () {'b': 10, 'a': 5}
	# Time of execution of function foo is 0.0069141387939453125 ms.
	# 15
