use strict;
use warnings;
use MaterialsScript qw(:all);

my $input_path = $ARGV[0] or die "Input structure path is required\n";
my $target_documents_dir = $ARGV[1] or die "Target Documents directory is required\n";
my $output_name = $ARGV[2] or die "Output document name is required\n";

my $output_path = $target_documents_dir;
$output_path .= "\\" unless $output_path =~ /[\\\/]$/;
$output_path .= $output_name;

my $doc = Documents->Import($input_path);
$doc->Export($output_path, Settings(Version => "2023", OmitNewerContent => "No"));
print "published_to_project_documents_ok\n";
print $output_path . "\n";
