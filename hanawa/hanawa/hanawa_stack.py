from aws_cdk import (
    # Duration,
    aws_ec2 as ec2,
    Stack,
)
from constructs import Construct

class HanawaStack(Stack):

    def __init__(self, scope: Construct, construct_id: str, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

        # The code that defines your stack goes here

        # example resource
        # queue = sqs.Queue(
        #     self, "HanawaQueue",
        #     visibility_timeout=Duration.seconds(300),
        # )
        # Create VPC
        vpc = ec2.Vpc(
            self,
            id="vpc",
            cidr="10.0.0.0/16",
            nat_gateways=0, # NatGatewayを作成しない指定
            # Create Private Subnet
            subnet_configuration=[
                ec2.SubnetConfiguration(
                    name="subnet",
                    subnet_type=ec2.SubnetType.PUBLIC,
                    cidr_mask=24
                )
            ]
        )
        
        # Create SecurityGroup
        security_group = ec2.SecurityGroup(
            self,
            id="hanawa-ec2-sg",
            vpc=vpc,
            allow_all_outbound=True,
            security_group_name="hanawa-ec2-sg"
        )

        # Add Ingress Rule
        security_group.add_ingress_rule(
            peer=ec2.Peer.ipv4("0.0.0.0/0"),
            connection=ec2.Port.tcp(22),
            description="allow ssh access"
        )

#        key = ec2.KeyPair(self,
#            key_pair_name="hanawa-keypair",
#            type=ec2.KeyPairType.RSA
#        )
        key_pair = ec2.KeyPair(self, "hanawa-KeyPair",
            type=ec2.KeyPairType.RSA,
            format=ec2.KeyPairFormat.PEM
        )
        # Create EC2
        ec2_instance = ec2.Instance(
            self,
            id="hanawa-ec2-instance",
            instance_type=ec2.InstanceType.of(
                ec2.InstanceClass.BURSTABLE2,
                ec2.InstanceSize.MICRO
            ),
            machine_image=ec2.AmazonLinuxImage(),
            vpc=vpc,
            vpc_subnets=ec2.SubnetSelection(
                subnet_type=ec2.SubnetType.PUBLIC
            ),
            instance_name="hanawa-ec2-instance",
            security_group=security_group,
            key_pair=key_pair
        )