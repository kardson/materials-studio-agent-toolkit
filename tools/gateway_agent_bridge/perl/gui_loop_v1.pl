use strict;
use warnings;
use MaterialsScript qw(:all);

my $root = 'C:/Users/kards/Documents/DFT/tools/gui_loop_queue';
my $pending = "$root/pending";
my $running = "$root/running";
my $done = "$root/done";
my $failed = "$root/failed";
my $logs = "$root/logs";

foreach my $dir ($root, $pending, $running, $done, $failed, $logs) {
    mkdir $dir unless -d $dir;
}

sub json_quote {
    my ($value) = @_;
    $value = '' unless defined $value;
    $value =~ s/\\/\\\\/g;
    $value =~ s/"/\\"/g;
    $value =~ s/\r/\\r/g;
    $value =~ s/\n/\\n/g;
    return '"' . $value . '"';
}

sub write_text_file {
    my ($path, $body) = @_;
    open(my $fh, '>', $path) or die "Cannot write $path: $!";
    print $fh $body;
    close($fh);
}

sub write_status_file {
    my ($path, $script, $started_at, $finished_at, $ok, $stdout_file, $error_message) = @_;
    my $body = "{\n"
        . '  "script": ' . json_quote($script) . ",\n"
        . '  "started_at": ' . json_quote($started_at) . ",\n"
        . '  "finished_at": ' . json_quote($finished_at) . ",\n"
        . '  "ok": ' . ($ok ? 'true' : 'false') . ",\n"
        . '  "stdout_file": ' . json_quote($stdout_file) . ",\n"
        . '  "error_message": ' . ($error_message ? json_quote($error_message) : 'null') . "\n"
        . "}\n";
    write_text_file($path, $body);
}

while (1) {
    opendir(my $dh, $pending) or die "Cannot open $pending: $!";
    my @jobs = sort grep { /\.pl$/i && -f "$pending/$_" } readdir($dh);
    closedir($dh);

    if (!@jobs) {
        sleep 3;
        next;
    }

    my $job = $jobs[0];
    my $src = "$pending/$job";
    my $run = "$running/$job";
    my $done_path = "$done/$job";
    my $fail_path = "$failed/$job";
    my $stdout_path = "$logs/$job.stdout.txt";
    my $status_path = "$logs/$job.status.json";

    rename $src, $run or die "Cannot move $src to running\n";

    my $started_at = scalar(localtime());
    my $ok = eval { do $run; die $@ if $@; 1; };
    my $finished_at = scalar(localtime());

    if ($ok) {
        rename $run, $done_path or die "Cannot move $run to done\n";
        write_text_file($stdout_path, "OK\n");
        write_status_file($status_path, $job, $started_at, $finished_at, 1, $stdout_path, undef);
    } else {
        my $err = $@ || "Unknown error";
        rename $run, $fail_path or die "Cannot move $run to failed\n";
        write_text_file($stdout_path, $err);
        write_status_file($status_path, $job, $started_at, $finished_at, 0, $stdout_path, $err);
    }
}
