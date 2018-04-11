from copy import copy

from troposphere import efs, Output, Tags

from stacker.blueprints.base import Blueprint
from stacker.blueprints.variables.types import CFNString


class ElasticFileSystem(Blueprint):
    VARIABLES = {
        'Tags': {
            'type': dict,
            'description': 'An optional dictionary of tags to put on the '
                           'FileSystem',
            'default': {}
        },
        'Encrypted': {
            'type': bool,
            'description': (
                'Encrypt the file system (default: false) update requires '
                'replacement'
            ),
            'default': False
        },
        'KmsKeyId': {
            'type': CFNString,
            'description': (
                'Optional: The ID of the AWS KMS customer master key (CMK) '
                'to use to protect the encrypted file system. required for '
                'non-default CMK. update requires replacement'
            ),
            'default': ''
        },
        'PerformanceMode': {
            'type': CFNString,
            'description': (
                'The performance mode of the file system `generalPurpose` or '
                '`maxIO` (default: generalPurpose) update requires replacement'
            ),
            'default': 'generalPurpose'
        },
    }

    def make_tags(self, tag_dict):
        t = {'Name': self.name}
        t.update(tag_dict)
        return Tags(**t)

    def create_filesystem(self):
        t = self.template
        params = copy(self.get_variables())

        if not params['KmsKeyId']:
            # Remove if blank
            params.pop('KmsKeyId')

        params['FileSystemTags'] = self.make_tags(params.pop('Tags'))

        self.file_system = t.add_resource(efs.FileSystem(**params))
        t.add_output(Output("FileSystem", Value=self.file_system))

    def create_template(self):
        self.create_filesystem()
