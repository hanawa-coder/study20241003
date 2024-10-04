import aws_cdk as core
import aws_cdk.assertions as assertions

from hanawa.hanawa_stack import HanawaStack

# example tests. To run these tests, uncomment this file along with the example
# resource in hanawa/hanawa_stack.py
def test_sqs_queue_created():
    app = core.App()
    stack = HanawaStack(app, "hanawa")
    template = assertions.Template.from_stack(stack)

#     template.has_resource_properties("AWS::SQS::Queue", {
#         "VisibilityTimeout": 300
#     })
