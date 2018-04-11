from stacker.context import Context
from stacker.config import Config
from stacker.variables import Variable

from stacker_blueprints.efs import ElasticFileSystem

from stacker.blueprints.testutil import BlueprintTestCase


class TestElasticFileSystem(BlueprintTestCase):
    def setUp(self):
        self.ctx = Context(config=Config({'namespace': 'test'}))

    def test_efs_defaults(self):
        blueprint = ElasticFileSystem('efs_a', self.ctx)
        # There are no required variables
        blueprint.resolve_variables([])
        blueprint.create_template()
        self.assertRenderedBlueprint(blueprint)

    def test_efs_tagging(self):
        blueprint = ElasticFileSystem('efs_b', self.ctx)
        blueprint.resolve_variables(
            [
                Variable('Tags', {'fancy': 'pants'}),
            ]
        )
        blueprint.create_template()
        self.assertRenderedBlueprint(blueprint)
