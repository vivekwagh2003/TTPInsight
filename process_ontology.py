import helper  # Importing a helper module (assumed to contain file reading/writing functions)
import json   # Importing JSON module for handling structured data
import re     # Regular expressions for text processing
import configuration  # Importing configuration module (assumed for settings management)

# File path for ontology examples
file_name = 'ontology/examples/ontology_from_examples.csv'

# Function to clean and shrink ontology data, removing duplicates
def shrink_example_ontology():
    # Read the CSV file into a list of dictionaries
    ontology_list = helper.read_csv_file(file_name=file_name)
    print('Total Length: ', len(ontology_list))
    shrinked_list = list()
    
    # Normalize and clean each ontology entry
    for ontology in ontology_list:
        new_dict = {
            'id': ontology['id'].lower().strip(),  # Convert 'id' to lowercase and remove spaces
            'what': ontology['what'].lower().replace(',', ' ').strip(),  # Remove commas from 'what'
            'where': ontology['where'].lower().replace(',', ' ').replace('"', '').strip()  # Clean 'where' field
        }
        # Convert to JSON string to allow easy deduplication
        shrinked_list.append(json.dumps(new_dict))
    
    # Remove duplicates by converting back to a list of dictionaries
    shrinked_list = list(set(shrinked_list))
    ontology_list = [json.loads(ontology) for ontology in shrinked_list]
    
    # Write the cleaned ontology data to a new CSV file
    helper.write_csv_from_dictionary('ontology/examples/ontology_from_examples_1.csv', ontology_list)
    print('Total Length: ', len(shrinked_list))

# Function to remove extra spaces in the 'where' field
def filter_spaces(file_name='ontology/examples/ontology_from_examples_1.csv'):
    # Read the cleaned ontology file
    ontology_list = helper.read_csv_file(file_name=file_name)
    print('Total Length: ', len(ontology_list))
    shrinked_list = list()
    
    # Process each ontology entry to normalize spacing
    for ontology in ontology_list:
        new_dict = {
            'id': ontology['id'],
            'what': ontology['what'],
            'where': ' '.join(ontology['where'].split())  # Remove multiple spaces
        }
        shrinked_list.append(new_dict)
    
    # Save the further cleaned data to another file
    helper.write_csv_from_dictionary('ontology/examples/ontology_from_examples_2.csv', shrinked_list)
    print('Total Length: ', len(shrinked_list))

# Regular expression pattern to extract text inside square brackets
symantec_description_pattern = re.compile(r'\[(.*?)\]')

# Function to process a description and extract structured key-value pairs
def process_single_AllenNLP_description(single_extraction_description):
    # Find all bracketed text (e.g., "[Action: Phishing]")
    match = symantec_description_pattern.findall(single_extraction_description)
    single_extraction_dictionary = dict()
    
    # Extract key-value pairs
    for results in enumerate(match):
        tuples = results[1]  # Extract matched text
        arg_name = tuples[:tuples.find(':')].strip()  # Extract key before ':'
        arg_val = tuples[tuples.find(':') + 1:].strip()  # Extract value after ':'
        single_extraction_dictionary[arg_name] = arg_val  # Store in dictionary
    
    return single_extraction_dictionary  # Return extracted key-value pairs

# Main execution block
if __name__ == '__main__':
    # Uncomment the below line if you want to shrink ontology
    # shrink_example_ontology()
    
    # Remove extra spaces from 'where' field
    filter_spaces()
