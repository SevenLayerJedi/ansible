#!/usr/local/bin/python
import os
import yaml


def create_yaml(filename, **kwargs):
    """
    Write YAML file with the provided properties.

    Parameters:
    - filename (str): Name of the YAML file to be created.
    - **kwargs: Key-value pairs representing the properties to be written to the YAML file.
    """
    # Write the configuration data to a YAML file
    with open(filename, 'w') as file:
        yaml.dump(kwargs, file)


def update_yaml(filename, **kwargs):
    """
    Update specified properties in a YAML file.

    Parameters:
    - filename (str): Name of the YAML file to be updated.
    - **kwargs: Key-value pairs representing the properties to be updated.
    """
    # Read the existing YAML file to get the current properties
    with open(filename, 'r') as file:
        config_data = yaml.safe_load(file)
    #
    # Update the specified properties
    for key, value in kwargs.items():
        if key in config_data:
            config_data[key] = value
        else:
            print(f"Warning: Property '{key}' does not exist in the YAML file.")
    #
    # Write the updated properties back to the YAML file
    with open(filename, 'w') as file:
        yaml.dump(config_data, file)







# Example Update
update_yaml('config.yaml', job_start='awawdawdawd', job_status='completed')



# Example usage:
create_yaml('config.yaml',
           job_id='',
           job_start='',
           job_end='',
           job_status='',
           cmd_name='',
           target_type='',
           task_description='',
           target_destination='',
           cmd='')




