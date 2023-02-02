from dtuhpc.jobwriter.commands import Command
from dtuhpc.jobwriter.job_writer import JobWriter
from dtuhpc.jobwriter.options import (
    ErrorOutputFilePathOption,
    MemoryPerCoreOption,
    NameOption,
    NCPUCoresOption,
    QueueOption,
    SingleHostOption,
    StandardOutputFilePathOption,
    WallTimeOption,
)

job_writer = JobWriter()

job_writer.add_option(QueueOption("hpc"))
job_writer.add_option(NameOption("testjob"))
job_writer.add_option(WallTimeOption(0, 15))
job_writer.add_option(NCPUCoresOption(2))
job_writer.add_option(SingleHostOption())
job_writer.add_option(MemoryPerCoreOption(4))
job_writer.add_option(StandardOutputFilePathOption("testjob.out"))
job_writer.add_option(ErrorOutputFilePathOption("testjob.err"))

job_writer.add_command(Command("echo 'Hello World'"))

job_writer.to_stdout()
