use strict;
use warnings;

print "ENV_PROBE_BEGIN\n";
print "PERL5LIB=" . ($ENV{PERL5LIB} // "") . "\n";
print "\@INC_BEGIN\n";
foreach my $path (@INC) {
    print "$path\n";
}
print "\@INC_END\n";

use lib 'C:/Program Files (x86)/BIOVIA/Materials Studio 24.1 x64 Server/lib/perl';
use lib 'C:/Program Files (x86)/BIOVIA/Materials Studio 24.1 x64 Server/lib/site_perl/5.36.0';

eval {
    require Filter::Util::Call;
    print "FILTER_UTIL_CALL_OK\n";
    1;
} or do {
    print "FILTER_UTIL_CALL_ERR=$@\n";
};

eval {
    require Switch;
    print "SWITCH_OK\n";
    1;
} or do {
    print "SWITCH_ERR=$@\n";
};

eval {
    require MaterialsScript;
    MaterialsScript->import(qw(:all));
    print "MATERIALSSCRIPT_OK\n";
    1;
} or do {
    print "MATERIALSSCRIPT_ERR=$@\n";
};

print "ENV_PROBE_END\n";
