use strict;
use warnings;
use MaterialsScript qw(:all);

my $output = 'C:/Users/kards/Documents/DFT/tools/gateway_agent_bridge/gui_context_probe_output.txt';
open(my $fh, '>', $output) or die "Cannot write $output: $!";

print $fh "GUI_CONTEXT_PROBE_BEGIN\n";

my $count = 0;
eval { $count = Documents->Count; };
print $fh "DOCUMENT_COUNT=$count\n";

for (my $i = 0; $i < $count; $i++) {
    my $doc = Documents->Item($i);
    my $name = '';
    eval { $name = $doc->Name; };
    print $fh "DOCUMENT[$i]=$name\n";
}

my $active_name = '';
my $active_doc = undef;
eval {
    $active_doc = Documents->ActiveDocument;
    $active_name = $active_doc->Name if $active_doc;
};
print $fh "ACTIVE_DOCUMENT=$active_name\n";

if ($active_doc) {
    my $atoms_count = '';
    eval {
        my $atoms = $active_doc->Atoms;
        $atoms_count = $atoms->Count if $atoms;
    };
    if ($atoms_count eq '') {
        eval {
            my $atoms = $active_doc->AsymmetricUnit->Atoms;
            $atoms_count = $atoms->Count if $atoms;
        };
    }
    print $fh "ACTIVE_ATOMS_COUNT=$atoms_count\n" if $atoms_count ne '';
}

print $fh "GUI_CONTEXT_PROBE_END\n";
close($fh);
print "gui_context_probe_ok\n";
