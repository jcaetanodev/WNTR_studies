# pickling.py
import pickle

class example_class:
    a_number = 35
    a_string = 'hey'
    a_list = [1, 2, 3]
    a_dict = {"first": "a", "second": 2, "third": [1, 2, 3]}
    a_tuple = (22, 23)

my_object = example_class()

# my_pickled_object = pickle.dump(my_object) # pickling the object
# print(f"This is my pickled object:\n{my_pickled_object}\n")

# my_object.a_dict = None
# my_unpickled_object = pickle.loads(my_pickled_object)  # Unpickling the object
# print(f"This is a_dict of the unpickled object:\n{my_unpickled_object.a_dict}\n")


with open('filename.pickle', 'wb') as handle:
    pickle.dump(my_object, handle, protocol=pickle.HIGHEST_PROTOCOL)

with open('filename.pickle', 'rb') as handle:
    b = pickle.load(handle)

print(b.a_number)