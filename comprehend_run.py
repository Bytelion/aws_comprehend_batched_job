from bs4 import BeautifulSoup as Soup
import boto3
import json

client = boto3.client('comprehend')

temp = open('./input_file/catted_file', 'r').read()
soup = Soup(temp,"html.parser")
bodies = soup.findAll('body')

file = open('./output/body.txt', 'w')
for body in bodies:
    the_contents_of_body_without_body_tags = body.findAll('p')
    final_results=""
    for item in the_contents_of_body_without_body_tags:
        final_results = final_results+" " + item.getText()+"\n"

    file.write(final_results)

file.close()

temp = open('./output/body.txt', 'r').read()
strings = temp.split(" ");

counter = 0;
aws_submission = "";
submission_counter = 0;
aws_queued_objects = []

for word in strings:

    pre_add_submission = aws_submission
    aws_submission = aws_submission + " " + word

    if len(aws_submission.encode('utf-8')) >5000:
        submission_counter = submission_counter+1
        print ("Submission Number = " + str(submission_counter) + " with a byte size of "+ str(len(pre_add_submission.encode('utf-8'))))

        aws_queued_objects.append(pre_add_submission)
        aws_submission = ""

response = client.batch_detect_entities(
    TextList=aws_queued_objects,LanguageCode='en')

json_aws_output = open('./output/entities.json', 'w')
json.dump(response, json_aws_output)
json_aws_output.close()

print ("done")