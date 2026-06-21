use strict;
use warnings;
use MaterialsScript qw(:all);

my $input_path = $ARGV[0] or die "Input structure path is required\n";
my $output_path = $ARGV[1] or die "Output structure path is required\n";

my $doc = Documents->Import($input_path);
$doc->Export($output_path, Settings(Version => "2023", OmitNewerContent => "No"));
print "published_to_project_documents\n";
