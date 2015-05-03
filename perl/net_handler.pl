#!/usr/bin/perl
use Expect;
$Expect::Log_Stdout = 1;

$IP = "192.168.1.106";
$password = "520fang";
$user = "fangfang";
$commnad_file = "cmd_list.txt";

open(CMD_list, '<', $commnad_file) or die "Could not open file $commnad_file $!";

my ($host,$pass) = ($IP,$password);
my $exp = Expect->new;
$exp = Expect->spawn("ssh -l $user $host");
$exp->log_file("output.log", "w");
$exp->expect(2,[
        qr/password:/i,
        sub {
            my $self = shift ;
            $self->send("$pass\n");
            exp_continue;
        }
    ],
    [
        'connecting (yes/no)',
        sub {
            my $self = shift ;
            $self->send("yes\n");
        }
    ]
);

foreach $cmd (<CMD_list>){
    chomp($cmd);
    $exp->send("$cmd\n") if ($exp->expect(undef,'~'));
}
$exp->send("exit\n") if ($exp->expect(undef,'~'));
$exp->log_file(undef);
$exp->interact() if ($exp->expect(undef,'~'));
close ($CMD_list);
