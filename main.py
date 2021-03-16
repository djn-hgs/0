import dateutil.parser as dp

# Where to save the FileExistsError

FILENAME = 'my_todo.csv'

# How to store a todo list

class TaskList(list):
  def add_item(self, todo):
    self.append(todo)
  
  def get_item(self, index):
    return self[index]
  
  def __str__(self):
    return '\n'.join([str(a) for a in self])

  def enumerate(self):
    enum_dict = {}

    counter = 1

    for i in self:
      enum_dict[str(counter)] = i
      counter += 1

    return enum_dict

# How to store a ToDo item

class ToDo:
  def __init__(self, description, due_date, status='Pending'):
    self.description = description
    self.due_date = Date(due_date)
    self.status = Status(status)
  
  def __str__(self):
    return f'{self.due_date} - \t{self.description}\t - {self.status}'
  
  def csv(self):
    return f'{repr(self.due_date)},{repr(self.description)},{repr(self.status)}\n'

  def mark_done(self):
    self.status.mark_done()

  def mark_undone(self):
    self.status.mark_undone()

# Handle date entry
# TODO: Proper validation

class Date:
  def __init__(self, date_str):
    self.date = dp.parse(date_str)
  
  def __repr__(self):
    return str(self.date.date())

# Handle task status

class Status:
  def __init__(self, status="Pending"):
    if status == 'Completed':
      self.done = True
    else:
      self.done = None

  def __repr__(self):
    if self.done:
      return 'Completed'
    else:
      return 'Pending'
  
  def mark_done(self):
    self.done = True
  
  def mark_undone(self):
    self.done = False
 

# A class to enable me to store an option list nicely

class OptionsList:
  def __init__(self):
    self.option_list = []

  def __str__(self):
    return '\n'.join([str(o) for o in self.option_list])

  def prompt(self):
    return '\n'.join([o.prompt() for o in self.option_list])  
  
  def add_option(self, option):
    self.option_list.append(option)
  
  def get_choice(self, char):
    choice = None

    for option in self.option_list:
      if option.check(char):
        choice = option
    
    return choice

# An option to go into the option list

class Option:
  def __init__(self, text, chars, func):
    self.text = text
    self.chars = chars
    self.func = func

  def __str__(self):
    return f'{self.text}'

  def prompt(self):
    char_list = ''.join(self.chars)
    return f'{self.text} ({char_list})'

  def check(self, char):
    return char in self.chars

  def call(self, task_list):
    return self.func(task_list)

# Procedure to mark an item done

def mark_done(task_list):
  tasks = t.enumerate()

  for k, v in tasks.items():
    print(f'{k}: {v}')

  # Keep asking until we get something sensible

  making_choice = True

  while making_choice:
    choice = input('Choose item to mark done: ')
    if choice in tasks.keys():
      making_choice = False
    
  tasks[choice].mark_done()

# Procedure to add an entry

def add_entry(task_list):
  task_description = input('Task description: ')
  task_due_date = input('Due date:')

  task_list.add_item(ToDo(task_description, task_due_date))

# Procedure to delete an entry

def del_entry(task_list):
  tasks = task_list.enumerate()

  for k, v in tasks.items():
    print(f'{k}: {v}')

  # This needs parsing

  making_choice = True

  choice_list = []

  while making_choice:
    choice = input('Choose item to delete: ')

    # Look for comma-separated choices

    if ',' in choice:
      choice_list = choice.split(',')
      if all(c in tasks for c in choice_list):
        making_choice = False
    
    # Look for a range using a hyphen

    elif '-' in choice:
      first, last = choice.split('-')
      first_num = int(first)
      last_num = int(last)

      for i in range(first_num, last_num + 1):
        if str(i) in tasks:
          choice_list.append(str(i))
        making_choice = False

    # Or is it an individual choice

    elif choice in tasks:
      choice_list = [choice]
      making_choice = False

  # Have a think about this: why am I ok to do this in place?

  for c in choice_list:
    task_list.remove(tasks[c])

# Procedure to load our data

def load_list(task_list):
  with open(FILENAME, "r") as fh:
    for line in fh:
      [date, description, status] = line.split(',')

      # Remove EOL characters from the last entry

      status = status.rstrip('\r\n')

      # Recover text from our formatted text

      description = eval(description)

      # Create task

      task_list.add_item(ToDo(description, date, status))

# Procedure to save our data

def save_list(task_list):
  with open(FILENAME, "w") as fh:
    for t in task_list:
      fh.write(t.csv())

# Store the options nicely. Over-engineered.

option_list = OptionsList()

option_list.add_option(Option('Mark done', ['M', 'm'], mark_done))
option_list.add_option(Option('Add entry', ['A', 'a'], add_entry))
option_list.add_option(Option('Delete entry', ['D', 'd'], del_entry))
option_list.add_option(Option('Load list', ['L', 'l'], load_list))
option_list.add_option(Option('Save list', ['S', 's'], save_list))

# Create a task list with a couple of fake entries

t = TaskList()

t.add_item(ToDo('Finish todo app', 'December 2 2020'))
t.add_item(ToDo('Something else', '13/12/20'))


# Main loop

running = True

while running:
  tasks = t.enumerate()

  for k, v in tasks.items():
    print(f'{k}: {v}')

  # Let's make sure we get a valid choice

  waiting_for_choice = True

  while waiting_for_choice:
    print('Selection available:')
    print(option_list.prompt())
    char = input("What's your choice? ")

    your_choice = option_list.get_choice(char)

    if your_choice:
      waiting_for_choice = False
    else:
      print('Please make a valid choice.')

  print(f'{your_choice}')   

  your_choice.call(t)
