#!perl
use strict;
use warnings;
use MaterialsScript qw(:all);

# GUI-resident thin dispatcher with explicit stop protocol.
# Run from Materials Studio GUI on Client with any document.

my $queue_root = $ENV{"MS_AGENT_QUEUE_DIR"} || "C:\\Users\\kards\\Documents\\DFT\\tools\\gui_loop_queue";
my $sleep_seconds = $ENV{"MS_AGENT_LOOP_SLEEP"} || 2;

my $pending = "$queue_root\\pending";
my $running = "$queue_root\\running";
my $done = "$queue_root\\done";
my $failed = "$queue_root\\failed";
my $held = "$queue_root\\held";
my $logs = "$queue_root\\logs";
my $stop_file = "$queue_root\\stop";
my $started_marker = "$queue_root\\gui_loop_started.txt";
my $status_file = "$queue_root\\gui_loop_status.txt";

foreach my $dir ($queue_root, $pending, $running, $done, $failed, $held, $logs) {
    mkdir $dir unless -d $dir;
}

sub write_text {
    my ($path, $body) = @_;
    open(my $fh, ">", $path) or die "Cannot write $path: $!";
    print $fh $body;
    close($fh);
}

sub append_text {
    my ($path, $body) = @_;
    open(my $fh, ">>", $path) or die "Cannot append $path: $!";
    print $fh $body;
    close($fh);
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

sub write_status_json {
    my ($path, $script, $started_at, $finished_at, $ok, $stdout_file, $error_message) = @_;
    my $body = "{\n"
        . '  "script": ' . json_quote($script) . ",\n"
        . '  "started_at": ' . json_quote($started_at) . ",\n"
        . '  "finished_at": ' . json_quote($finished_at) . ",\n"
        . '  "ok": ' . ($ok ? 'true' : 'false') . ",\n"
        . '  "stdout_file": ' . json_quote($stdout_file) . ",\n"
        . '  "error_message": ' . ($error_message ? json_quote($error_message) : 'null') . "\n"
        . "}\n";
    write_text($path, $body);
}

sub write_status_line {
    my ($status, $job, $detail) = @_;
    append_text(
        $status_file,
        scalar(localtime()) . "\t$status\t" . ($job || "") . "\t" . ($detail || "") . "\n"
    );
}

append_text($started_marker, "GUI loop v2 started at " . scalar(localtime()) . "\n");
print "GUI loop v2 started\n";
print "Queue: $queue_root\n";
write_status_line("started", "gui_loop_v2", $queue_root);

my $last_heartbeat = 0;

while (1) {
    last if -e $stop_file;

    my $now = time();
    if ($now - $last_heartbeat >= 30) {
        write_status_line("heartbeat", "gui_loop_v2", $queue_root);
        $last_heartbeat = $now;
    }

    opendir(my $dh, $pending) or die "Cannot open $pending: $!";
    my @jobs = sort grep { /\.pl$/i && -f "$pending\\$_" } readdir($dh);
    closedir($dh);

    if (!@jobs) {
        sleep($sleep_seconds);
        next;
    }

    my $job = $jobs[0];
    my $src = "$pending\\$job";
    my $active = "$running\\$job";
    my $ok_path = "$done\\$job";
    my $bad_path = "$failed\\$job";
    my $stdout_path = "$logs\\$job.stdout.txt";
    my $status_json = "$logs\\$job.status.json";

    next unless rename $src, $active;

    my $started_at = scalar(localtime());
    write_status_line("running", $job, "");
    print "Running $job\n";

    my $success = eval {
        do $active;
        die $@ if $@;
        1;
    };

    my $finished_at = scalar(localtime());

    if ($success) {
        rename $active, $ok_path or die "Cannot move $active to done";
        write_text($stdout_path, "OK\n");
        write_status_json($status_json, $job, $started_at, $finished_at, 1, $stdout_path, undef);
        write_status_line("done", $job, "");
        print "Finished $job\n";
    } else {
        my $error = $@ || "Unknown MaterialsScript error";
        write_text("$active.error.txt", $error);
        rename $active, $bad_path or die "Cannot move $active to failed";
        rename "$active.error.txt", "$bad_path.error.txt";
        write_text($stdout_path, $error);
        write_status_json($status_json, $job, $started_at, $finished_at, 0, $stdout_path, $error);
        write_status_line("failed", $job, $error);
        print "Failed $job: $error\n";
    }
}

unlink $stop_file if -e $stop_file;
write_status_line("stopped", "gui_loop_v2", "");
print "GUI loop v2 stopped\n";
