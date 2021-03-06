import en

BASIC = """
ability
above
absolute
accept
accord
achieve
action
actual
add
additional
adult
advise
affect
aft
agree
ahead
alive
allow
alone
already
although
america
american
apply
appear
areas
around
arrive
ask
assign
assume
attendance
available
avoid
basic
bear
begin
believe
below
benefit
beyond
big
biggest
binary
block
bound
brief
bring
broad
build
bus
buy
can
cannot
capture
car
carry
cash
catch
center
century
chapter
children
choose
city
close
collect
command
communication
compare
complexity
conclusion
conduct
confront
consequence
consider
considerable
consideration
contain
content
continue
correct
count
create
dad
datum
deal
decide
decline
defend
define
delay
depend
determine
develop
die
differ
differential
difficult
dig
discuss
double
draw
drive
during
earlier
earn
easier
easily
eat
educate
educational
else
emotion
english
enjoy
enter
equipment
essential
excellent
except
exist
expect
explain
extent
external
fail
farmers
fast
favor
feedback
feel
few
fewer
file
fill
film
final
find
fine
fit
fix
follow
forget
found
fun
function
gain
game
getting
goal
grade
greatest
grow
handful
happen
harder
hear
hi
higher
his
historic
hit
hot
huge
ignore
immediate
impression
include
increasing
independent
indicator
information
instead
internal
item
job
john
joy
just
kid
kill
know
knowledgeable
lack
lady
largest
later
lay
leader
learn
learned
leave
lie
limitation
listen
live
location
logical
lose
lot
mad
mail
main
major
manage
management
master
meet
mere
method
mike
minimize
miss
mistake
mobile
mode
modify
mom
moment
must
national
nationwide
necessarily
neither
nod
none
nor
notice
notion
object
objective
occur
official
often
older
operate
opportunity
ordinary
organize
original
others
paid
particular
pas
pass
pattern
pay
per
percent
perform
performance
period
personal
phrase
piece
policy
possess
powerful
practical
precise
prefer
prepare
press
prevent
principle
probably
problem
procedure
proceed
production
project
proper
prove
provide
publish
quit
raise
rank
rather
raw
reach
read
realize
receive
recommend
reduce
refer
regard
remember
repeat
repeated
reply
report
require
respond
return
richest
ride
risk
role
rush
save
scientific
score
seek
seldom
select
sell
serve
several
shall
shift
shop
should
sigh
similar
simplicity
simply
single
sit
site
situation
skill
slave
smart
solve
sometimes
soon
source
span
speak
specific
specify
speech
speed
spend
stand
state
stay
student
succeed
successful
suppose
sure
task
teach
technical
tell
tend
thank
themselves
think
throw
tip
title
toward
towards
transform
trend
truth
try
type
ultimate
understand
union
unless
until
useless
users
using
usual
variety
various
vary
vast
verification
virtual
visit
wait
walk
want
wealth
wear
whole
win
wish
women
wonder
worry
worse
worth
write
yet
younger
zero
zone
"""

BASIC = [x for x in BASIC.split("\n") if x]
basic_words = dict([(x, 1) for x in BASIC + en.basic.words])
