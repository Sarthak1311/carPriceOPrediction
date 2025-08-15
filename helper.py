# Python function to automatically create data.yaml config file
import yaml
import os

def create_data_yaml(path_to_classes_txt, path_to_data_yaml):

  # Read class.txt to get class names
  if not os.path.exists(path_to_classes_txt):
    print(f'classes.txt file not found! Please create a classes.txt labelmap and move it to {path_to_classes_txt}')
    return
  with open(path_to_classes_txt, 'r') as f:
    classes = []
    for line in f.readlines():
      if len(line.strip()) == 0: continue
      classes.append(line.strip())
  number_of_classes = len(classes)

  # Create data dictionary
  data = {
      'path': '/Users/sarthaktyagi/Desktop/30days-3oprojects/car_price_prediction/carDamageScore',
      'train': '/Users/sarthaktyagi/Desktop/30days-3oprojects/car_price_prediction/carDamageScore/images/train',
      'val': '/Users/sarthaktyagi/Desktop/30days-3oprojects/car_price_prediction/carDamageScore/images/val',
      'nc': number_of_classes,
      'names': classes
  }

  # Write data to YAML file
  with open(path_to_data_yaml, 'w') as f:
    yaml.dump(data, f, sort_keys=False)
  print(f'Created config file at {path_to_data_yaml}')

  return


path_to_classes_txt = '/Users/sarthaktyagi/Desktop/30days-3oprojects/car_price_prediction/carDamageScore/classes.txt'
path_to_data_yaml = '/Users/sarthaktyagi/Desktop/30days-3oprojects/car_price_prediction/dataset.yaml'

create_data_yaml(path_to_classes_txt, path_to_data_yaml)

print('\nFile contents:\n')
