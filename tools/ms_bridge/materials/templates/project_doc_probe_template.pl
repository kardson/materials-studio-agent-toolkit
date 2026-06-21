use strict;
use warnings;
use MaterialsScript qw(:all);

my $count = 0;
eval { $count = Documents->Count; };
for (my $i = 0; $i < $count; $i++) {
    my $doc = Documents->Item($i);
    my $name = "";
    eval { $name = $doc->Name; };
    print $name . "\n";
}
