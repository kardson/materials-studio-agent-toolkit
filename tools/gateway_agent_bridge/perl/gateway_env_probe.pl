use strict;
use warnings;

use lib 'C:/Program Files (x86)/BIOVIA/Materials Studio 24.1 x64 Server/lib/perl';

print "PERL5LIB=" . ($ENV{PERL5LIB} // "") . "\n";
print "\@INC_BEGIN\n";
foreach my $path (@INC) {
    print "$path\n";
}
print "\@INC_END\n";

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
