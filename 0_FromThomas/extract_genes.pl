# This is the PCG extracting script used in the MSc practicals. Wirtten in Perl
# Execute: perl extract_genes.pl -genbank PlayData.gb -out . -regiontypes CDS
# Help: perl extract_genes.pl -h

# Check all values of reqregion make sense
die "Error: one or more region names given to -reqregion don't match any known gene names\n" unless scalar (intersect(@reqregion, @$known_genes)) == scalar @reqregion;

# Check all values of regiontypes make sense
my @alltypes = ('CDS', 'rRNA', 'tRNA');
die "Error: supply one or more region types to -regiontypes\n" unless scalar @regiontypes > 0;
die "Error: one or more region types given to -regiontypes don't match any known region types\n" unless scalar (unique(@regiontypes, @alltypes)) == 3;

my %regtypes = map {$_ => 1} @regiontypes;

# Make output directory
make_path($outdir);

# Set up fasta objects for outputs
my %faobjs;

# Set up hash for unrecognised gene names
my %unrec_genes;

# Work through genbank files
foreach my $gbp (@gbpaths){
	
	# Initialise genbank read object
	my $gb_in = Bio::SeqIO->new(-file => $gbp,
				    -format => "genbank",
				    -verbose => -1);
	
	# Work through sequences in object
	while(my $seq = $gb_in->next_seq){
		
		$seq->verbose(-1);
		
		# Extract sequence name
		my $seqname = $seq->display_id;
		
		# Get all features with sufficient identification from object
		my @all_feats = grep {$_->has_tag('gene') or $_->has_tag('product') or $_->has_tag('label')} ($seq->get_SeqFeatures);
		
		# Set up containers
		my %found_genes;
		my $checked_features = 0;
		
		#printf "Seqname = $seqname, Feats = %d, max_checked_feats = %d\n", $#all_feats, $#all_feats * 2 + 1;
		
		# Work through features to extract data
		while($checked_features < ($#all_feats * 2 + 1) and scalar keys %found_genes < scalar @all_feats){
			
			# Assess current position in search
			my $round = $checked_features <= $#all_feats ? 0 : 1;
			my $i = $round ? $checked_features - $#all_feats - 1 : $checked_features;
			
			# Extract feature
			my $feat = $all_feats[$i];
			$feat->verbose(-1);
			
			my $feattype = $feat->primary_tag;
			
			# Get clean gene name and convert
			my $gene = get_clean_name($feat);
			$gene = ${$genesort}{$gene} if ${$genesort}{$gene};
			
			#print "Checked_features = $checked_features, Round = $round, i = $i, feattype = $feattype, gene = $gene ...";
			
			
			# If gene has not already been extracted, it is the first round of checks and this is a required type of feature or it is the second round of checks and this is a gene feature and the gene type matches those required
			
			if( not $found_genes{$gene} and 
					( $regtypes{$feattype} or (
						$feat->primary_tag eq 'gene' and 
						$round and 
						${$generegion}{$gene} and 
						$regtypes{${$generegion}{$gene}}
						)
					)){
				#print "extracting\n";
				
				# Make a new output object for this gene if needed
				if(! $faobjs{$gene}){
					$faobjs{$gene} = Bio::SeqIO->new(-file => ">${outdir}/$gene.fa",
									 -format => "fasta");
				}
				
				# Compile output sequence object and store
				my $outseq = $feat->seq;
				$outseq->display_id($seqname);
				$outseq->description("");
				$outseq->verbose(-1);
				
				$found_genes{$gene} = $outseq;
				
				# Add to unrecognised genes if unrecognised
				push @{$unrec_genes{$gene}}, $seqname unless ${$genesort}{$gene};
			} else {
				#print "skipping\n";
			}
			$checked_features++;
		}
		
		# Run checks against threshold number and content of found genes
		my @found_gene_names = keys %found_genes;
		my $n_found_known_genes = scalar (intersect( @found_gene_names, @{$known_genes}));
		warn "Sequence $seqname in $gbp has $n_found_known_genes known features with sufficient information, it will be skipped\n" and next unless $n_found_known_genes >= $minregion;
		
		warn "Sequence $seqname in $gbp does not include all required regions, it will be skipped\n" and next if scalar (intersect(@reqregion, @found_gene_names)) < scalar @reqregion and @reqregion;
		
		# Write out found genes
		$faobjs{$_}->write_seq($found_genes{$_}) foreach(keys %found_genes);
		
	}
}

if(scalar keys %unrec_genes > 0){
	print "Excess files due to unrecognised gene names:\n", join (", ", keys %unrec_genes), "\n\nSource sequences of unrecognised gene names:\n" ;
	
	foreach my $ugene (keys %unrec_genes){
		print "$ugene: ", join (", ", @{$unrec_genes{$ugene}}), "\n";
	}
}

exit;

sub sort_genes{
	my ($genenametxt) = @_;
	my @genenames;
	my %genesort;
	my %generegion;
	foreach my $line (split("\n", $genenametxt)){
		my @values = split("[;:,]", $line);
		push @genenames, $values[0];
		$generegion{$values[0]} = $values[1];
		foreach my $var (@values[2..$#values]){
			$genesort{$var} = $values[0];
		}
	}
	return(\@genenames, \%genesort, \%generegion)
}

sub get_clean_name{
	my ($feat) = @_;
	my $name;
	
	if($feat->has_tag('gene')){
		($name) = $feat->get_tag_values('gene');
	} elsif($feat->has_tag('label')){
		($name) = $feat->get_tag_values('label');
	}
	if($name){
		$name = uc $name;
		$name =~ s/[(;_ ].*$//;
		$name =~ s/(?<!MT)-.*$//;
	} elsif($feat->has_tag('product')){
		($name) = $feat->get_tag_values('product');
		$name = uc $name;
	} else {
		die "Error: feature passed to get_clean_name subroutine without gene, label or product tag\n";
	}
	
	return($name)
}
