from aws_cdk import (
    # Duration,
    Stack,
    aws_ecs as ecs,
    aws_ec2 as ec2,
    aws_logs as logs,
    aws_ecr as ecr,
    aws_iam as iam,
)
from constructs import Construct


class InfraStack(Stack):
    def __init__(self, scope: Construct, construct_id: str, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

        self.cluster = self.get_cluster()
        self.dyn_service = self.get_dyn_service()

    def get_cluster(self):
        self.vpc = ec2.Vpc.from_lookup(
            self,
            "Vpc",
            vpc_id="vpc-849531e0",
        )
        cluster = ecs.Cluster.from_cluster_attributes(
            self,
            "cluster",
            cluster_name="test-btc",
            vpc=self.vpc,
            security_groups=[ec2.SecurityGroup(self, "sg", vpc=self.vpc)],
        )
        return cluster

    def get_dyn_service(self):
        task_definition = ecs.ExternalTaskDefinition(
            self,
            "TaskDef",
        )

        dyn_task = task_definition.add_container(
            "dyn-dns",
            image=ecs.ContainerImage.from_ecr_repository(
                ecr.Repository.from_repository_name(
                    self, "dyndnsecr", repository_name="dynamic-dns"
                )
            ),
            environment={
                "DOMAIN_NAME": "home.kloudcover.com",
                "HOSTED_ZONE": "kloudcover.com",
            },
            memory_reservation_mib=256,
            logging=ecs.LogDrivers.aws_logs(
                log_retention=logs.RetentionDays.ONE_WEEK, stream_prefix="dyn-dns"
            ),
        )
        task_definition.add_to_task_role_policy(
            iam.PolicyStatement(
                actions=[
                    "route53:ChangeResourceRecordSets",
                    "route53:ListResourceRecordSets",
                    "route53:GetHostedZone",
                    "route53:ListHostedZones",
                ],
                resources=["*"],
            )
        )
        ecs.ExternalService(
            self,
            "dyndns",
            cluster=self.cluster,
            task_definition=task_definition,
            service_name="dyn-dns",
        )
