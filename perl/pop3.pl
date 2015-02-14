use utf8;
use Socket;
use FileHandle;
use LWP::Simple;
use Courriel qw();
use Web::Query;
use HTML::Parser;
use open ':std', ':encoding(UTF-8)';
use List::MoreUtils qw(uniq);

sub main {
#pop3_read - pull in our email!
#($#ARGV > 1) || die "Usage: $0 <host> <user> <password> [CLEAR]\n";


my ($host, $user,$password,$arg3) = @_;
my $delete = ($arg3 eq "CLEAR");
my $trace =  0;

my $iaddr = inet_aton($host) or die "cant reach mail server";
my $paddr = sockaddr_in(110, $iaddr);
my $proto = getprotobyname("tcp");
socket(FHOST, PF_INET, SOCK_STREAM, $proto) or die "socket";
connect(FHOST, $paddr) or die "connect";

#turn buffering off
autoflush FHOST 1;

#dialogue
my $banner = <FHOST>;
$trace and print $banner;
print FHOST "user $user\r\n";
$banner = <FHOST>;
$trace and print $banner;
print FHOST "pass $password\r\n";
$banner = <FHOST>;
print FHOST "list\r\n";

my @stack;
while(1)
{
	my $next = <FHOST>;
	last if ($next =~ /^\./);
	$trace and print $next;
	push @stack, $next;
}

print (("x")x72, "\n");
print "received email num is ".$#stack."\n";
for(my $k = $#stack; $k >= 1; $k--)
{
	if ($k != $#stack )
	{
		next;
	}
	print FHOST "retr $k\r\n";
	$trace and print "retr $k\n";
	my $raw_email = "";
	my $okline = <FHOST>;
	while(my $line = <FHOST>)
	{
		last if ($line =~ /^\.\s*[\r\n]/);
		#print $line;
		$raw_email .= $line;
	}
	
	my $email = Courriel->parse(text=> $raw_email, is_character => 0);
	my $html = $email->html_body_part()->content();
	
	#open (INBOX, ">inbox.html");
	#print INBOX $html;
	#print $html;
	print (("x")x72,"\n");

	my $parser = HTML::Parser->new( text_h => [ sub { $_[0]->{_data} .= $_[1]; },"self,dtext" ],
                                start_document_h => [ sub { $_[0]->{_data} = '';}, "self"]);
	$parser->parse($html);
                                                                                
	print $parser->{_data};
	#print("\n\n");
	my $dealid_pattren = '\b\d+-[\d]{8}-\d+\b';
	my $chinese_pattern = '.*[\x{4e00}-\x{9fcc}]+.*';
	my $dealid_reg = eval {qr/$dealid_pattren/};
	my $chinese_reg = eval {qr/$chinese_pattern/};
    
    #if( my @all = $html =~ m/$dealid_reg/g)
    #{
    #	my @uniq_all = uniq @all;
    #	foreach(@uniq_all)
    #	{
    #		#print $_."\n";
    #	}
    #	
    #}else
    #{
    #	print "re failed!";
    #}
	
	if( my @all = $html =~ m/$chinese_reg/gs)
    {
    	#my @uniq_all = uniq @all;
    	foreach(@all)
    	{
    	#	print $_."\n";
    	}
    	
    }else
    {
    	print "re failed!";
    }
    

	if($delete)
	{
		print FHOST "dele $k\r\n";
		$trace and print "DELETING\n";
		my $resp = <FHOST>;
	}
}

print FHOST "quit\r\n";
}

main('','','');
