import boto3
import logging

logger = logging.getLogger('tagger')
logger.setLevel(logging.INFO)
logging.basicConfig()

def recieve_request(request):
	return request.instance_id

def tag_key_exists(tag,tags):
	if tags:
		if tag in tags:
			return True
	return False

def tag_valid(tag):
	if tag['Key'].startswith('aws'):
		return False
	return True

def copy_tags_to_volumes(instance_id):
	ec2 = boto3.resource('ec2')
	instance = ec2.Instance(instance_id)

	instance_tags = instance.tags
	volumes = instance.volumes.all()

	for volume in volumes:
		for instance_tag in instance_tags:
			if tag_valid(instance_tag):
				if not tag_key_exists(instance_tag,volume.tags):
					logger.info('Adding tag: ' + str(instance_tag))
					volume.create_tags(Tags=[instance_tag])
				else:
					logger.info('Tag key already exists: ' + str(instance_tag))
			else:
				logger.info('Tag invalid: ' + str(instance_tag))

if __name__ == '__main__':
	copy_tags_to_volumes('i-051d774324ff797a9')