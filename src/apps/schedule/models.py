from django.db import models


class Faculty(models.Model):
    id = models.BigAutoField(primary_key=True)
    name = models.CharField(max_length=255)
    display_name = models.CharField(max_length=255)
    short_display_name = models.CharField(max_length=255)

    class Meta:
        managed = False
        db_table = "faculties"

    def __str__(self) -> str:
        return self.display_name or self.name


class Insertion(models.Model):
    id = models.BigAutoField(primary_key=True)
    date = models.DateField()
    faculty = models.ForeignKey(
        Faculty,
        db_column="faculty_id",
        on_delete=models.DO_NOTHING,
        related_name="insertions",
    )
    hash = models.CharField(max_length=255)

    class Meta:
        managed = False
        db_table = "insertions"

    def __str__(self) -> str:
        return f"Insertion(id={self.id}, date={self.date}, faculty={self.faculty_id})"


class Building(models.Model):
    id = models.BigAutoField(primary_key=True)
    name = models.CharField(max_length=255)

    class Meta:
        managed = False
        db_table = "buildings"

    def __str__(self) -> str:
        return self.name


class Audience(models.Model):
    id = models.BigAutoField(primary_key=True)
    name = models.CharField(max_length=255)
    autocreated = models.BooleanField(default=False)
    building = models.ForeignKey(
        Building,
        db_column="building_id",
        on_delete=models.DO_NOTHING,
        related_name="audiences",
        default=4,
    )

    class Meta:
        managed = False
        db_table = "audiences"

    def __str__(self) -> str:
        return self.name


class Subdivision(models.Model):
    id = models.BigAutoField(primary_key=True)
    name = models.CharField(max_length=255)

    class Meta:
        managed = False
        db_table = "subdivisions"

    def __str__(self) -> str:
        return self.name


class Group(models.Model):
    id = models.BigAutoField(primary_key=True)
    name = models.CharField(max_length=255)
    faculty = models.ForeignKey(
        Faculty,
        db_column="faculty_id",
        on_delete=models.DO_NOTHING,
        related_name="groups",
    )

    class Meta:
        managed = False
        db_table = "groups"

    def __str__(self) -> str:
        return self.name


class Teacher(models.Model):
    id = models.BigAutoField(primary_key=True)
    login = models.CharField(max_length=255)
    name = models.CharField(max_length=255)
    url = models.CharField(max_length=2048)

    class Meta:
        managed = False
        db_table = "teachers"

    def __str__(self) -> str:
        return self.name


class Pair(models.Model):
    id = models.BigAutoField(primary_key=True)
    text = models.TextField()
    num = models.IntegerField()
    date = models.DateField()
    subject = models.CharField(max_length=255)

    insertion = models.ForeignKey(
        Insertion,
        db_column="insertion_id",
        on_delete=models.DO_NOTHING,
        related_name="pairs",
    )

    groups = models.ManyToManyField(
        Group,
        through="GroupsOfPairs",
        related_name="pairs",
    )
    teachers = models.ManyToManyField(
        Teacher,
        through="TeachersOfPairs",
        related_name="pairs",
    )
    audiences = models.ManyToManyField(
        Audience,
        through="AudiencesOfPairs",
        related_name="pairs",
    )

    class Meta:
        managed = False
        db_table = "pairs"

    def __str__(self) -> str:
        return f"Pair(id={self.id}, num={self.num}, date={self.date})"


class AudiencesOfSubdivisions(models.Model):
    audience = models.ForeignKey(
        Audience,
        db_column="audience_id",
        on_delete=models.DO_NOTHING,
        related_name="audiences_of_subdivisions",
    )
    subdivision = models.ForeignKey(
        Subdivision,
        db_column="subdivision_id",
        on_delete=models.DO_NOTHING,
        related_name="audiences_of_subdivisions",
    )

    class Meta:
        managed = False
        db_table = "audiencesofsubdivisions"
        constraints = [
            models.UniqueConstraint(
                fields=["audience", "subdivision"],
                name="uq_audiencesofsubdivisions_audience_subdivision",
            )
        ]


class AudiencesOfPairs(models.Model):
    audience = models.ForeignKey(
        Audience,
        db_column="audience_id",
        on_delete=models.DO_NOTHING,
        related_name="audiences_of_pairs",
    )
    pair = models.ForeignKey(
        Pair,
        db_column="pair_id",
        on_delete=models.DO_NOTHING,
        related_name="audiences_of_pairs",
    )

    class Meta:
        managed = False
        db_table = "audiencesofpairs"
        constraints = [
            models.UniqueConstraint(
                fields=["audience", "pair"],
                name="uq_audiencesofpairs_audience_pair",
            )
        ]


class GroupsOfPairs(models.Model):
    group = models.ForeignKey(
        Group,
        db_column="group_id",
        on_delete=models.DO_NOTHING,
        related_name="groups_of_pairs",
    )
    pair = models.ForeignKey(
        Pair,
        db_column="pair_id",
        on_delete=models.DO_NOTHING,
        related_name="groups_of_pairs",
    )

    class Meta:
        managed = False
        db_table = "groupsofpairs"
        constraints = [
            models.UniqueConstraint(
                fields=["group", "pair"],
                name="uq_groupsofpairs_group_pair",
            )
        ]


class TeachersOfPairs(models.Model):
    teacher = models.ForeignKey(
        Teacher,
        db_column="teacher_id",
        on_delete=models.DO_NOTHING,
        related_name="teachers_of_pairs",
    )
    pair = models.ForeignKey(
        Pair,
        db_column="pair_id",
        on_delete=models.DO_NOTHING,
        related_name="teachers_of_pairs",
    )

    class Meta:
        managed = False
        db_table = "teachersofpairs"
        constraints = [
            models.UniqueConstraint(
                fields=["teacher", "pair"],
                name="uq_teachersofpairs_teacher_pair",
            )
        ]
