use strict;
use warnings;
use MaterialsScript qw(:all);

my $target_name = 'S1_v2_GaAs100_6L_2x2_singleO_init.xsd';
my $result_name = 'CASTEP_S1_V2_5B_singleO_opt_gui.xsd';
my $settings_name = 'CASTEP_S1_V2_5B_singleO_opt_gui_settings';
my $log_path = 'gui_castep_go_s1_v2_5b_log.txt';
my $report_export_path = 'gui_castep_go_s1_v2_5b_report.txt';
my $result_export_path = 'gui_castep_go_s1_v2_5b_result.xsd';
my $doc_export_path = $result_name;

open(my $log, '>', $log_path) or die "Cannot write $log_path: $!";
print $log "GUI_CASTEP_GO_5B_BEGIN\n";
print $log "TARGET_NAME=$target_name\n";
print $log "SCRIPT_RESULTS_DIR=.\n";

my $doc = $Documents{$target_name};
die "Document not found in current project: $target_name\n" unless $doc;
print $log "FOUND_DOCUMENT=" . $doc->Name . "\n";

my $atom_count = $doc->AsymmetricUnit->Atoms->Count;
print $log "ATOM_COUNT=$atom_count\n";

my $working_doc = $doc->SaveAs($result_name);
print $log "WORKING_DOCUMENT=" . $working_doc->Name . "\n";

Modules->CASTEP->ChangeSettings(Settings(
    Quality => 'Coarse',
    PropertiesKPointQuality => 'Coarse',
    DipoleCorrection => 'Self-consistent'
));
print $log "CHANGESETTINGS_OK\n";

Modules->CASTEP->SaveSettings($settings_name);
print $log "SAVESETTINGS_OK=$settings_name\n";

my $results = Modules->CASTEP->GeometryOptimization->Run($working_doc, Settings(
    Quality => 'Coarse',
    PropertiesKPointQuality => 'Coarse',
    DipoleCorrection => 'Self-consistent'
));
print $log "RUN_RETURNED\n";

my $result_doc = $results->Structure;
print $log "RESULT_DOCUMENT=" . $result_doc->Name . "\n";

my $report = $results->Report;
$report->Export($report_export_path);
print $log "REPORT_EXPORTED=$report_export_path\n";

my $energy = $results->TotalEnergy;
print $log "TOTAL_ENERGY=$energy\n";

my $enthalpy = $results->Enthalpy;
print $log "ENTHALPY=$enthalpy\n";

my $converged = $results->Converged;
print $log "CONVERGED=$converged\n";

$result_doc->SaveAs($doc_export_path);
print $log "RESULT_DOC_SAVED_AS=$doc_export_path\n";
$result_doc->Export($result_export_path, Settings(Version => '2023', OmitNewerContent => 'No'));
print $log "RESULT_EXPORTED=$result_export_path\n";
$result_doc->Close;
print $log "RESULT_DOC_CLOSED\n";

print $log "GUI_CASTEP_GO_5B_END\n";
close($log);
print "gui_castep_go_s1_v2_5b_ok\n";
