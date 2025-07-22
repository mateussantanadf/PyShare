Firebird engine parallel features in v5.
----------------------------------------

Author: Vladyslav Khorsun <hvlad at users sourceforge net>


  The Firebird engine can now execute some tasks using multiple threads in
parallel. Currently parallel execution is implemented for the sweep and the
index creation tasks. Parallel execution is supported for both auto- and manual
sweep.

  To handle same task by multiple threads engine runs additional worker threads
and creates internal worker attachments. By default, parallel execution is not
enabled. There are two ways to enable parallelism in user attachment:
- set number of parallel workers in DPB using new tag isc_dpb_parallel_workers,
- set default number of parallel workers using new setting ParallelWorkers in
  firebird.conf.

  For gfix utility there is new command-line switch -parallel that allows to
set number of parallel workers for the "sweep" and "icu" tasks. For example:

  gfix -sweep -parallel 4 <database>

will run sweep on given database and ask engine to use 4 workers. gfix uses DPB
tag isc_dpb_parallel_workers when attaches to <database>, if switch -parallel
is present.

  New firebird.conf setting ParallelWorkers set default number of parallel
workers that can be used by any user attachment running parallelizable task.
Default value is 1 and means no use of additional parallel workers. Value in
DPB have higher priority than setting in firebird.conf.

  To control number of additional workers that can be created by the engine 
there are two new settings in firebird.conf: 
- ParallelWorkers - set default number of parallel workers that used by user 
  attachments. 
  Could be overriden by attachment using tag isc_dpb_parallel_workers in DPB.
- MaxParallelWorkers - limit number of simultaneously used workers for the
  given database and Firebird process.

  Internal worker attachments are created and managed by the engine itself.
Engine maintains per-database pools of worker attachments. Number of items in
each of such pool is limited by value of MaxParallelWorkers setting. The pools
are created by each Firebird process independently.

  In Super Server architecture worker attachments are implemented as light-
weight system attachments, while in Classic and Super Classic its looks like
usual user attachments. All worker attachments are embedded into creating
server process. Thus in Classic architectures there is no additional server
processes. Worker attachments are present in monitoring tables. Idle worker
attachment is destroyed after 60 seconds of inactivity. Also, in Classic
architectures worker attachments are destroyed immediately after last user
connection detached from database.


Examples:

  Set in firebird.conf ParallelWorkers = 4, MaxParallelWorkers = 8 and restart
Firebird server.

a) Connect to test database not using isc_dpb_parallel_workers in DPB and
execute "CREATE INDEX ..." SQL statement. On commit the index will be actually
created and engine will use 3 additional worker attachments. In total, 4 
attachments in 4 threads will work on index creation.

b) Ensure auto-sweep is enabled for test database. When auto-sweep will run on
that database, it also will use 3 additional workers (and run within 4 threads).

c) more than one single task at time could be parallelized: make 2 attachments
and execute "CREATE INDEX ..." in each of them (of course indices to be built
should be different). Each index will be created using 4 attachments (1 user
and 3 worker) and 4 threads.

d) run gfix -sweep <database> - not specifying switch -parallel: sweep will run
using 4 attachments in 4 threads.

d) run gfix -sweep -parallel 2 <database>: sweep will run using 2 attachments in
2 threads. This shows that value in DPB tag isc_dpb_parallel_workers overrides
value of setting ParallelWorkers.

