    def export(self, start, end, output_path=None, plain_header=False, separate_header=True,
               progress=None, deduplicate_transactions=True):
        """Export the blockchain into CSV files."""
        if output_path is None:
            output_path = 'blocks_{}_{}'.format(start, end)

        number_of_blocks = end - start + 1
        with CSVDumpWriter(output_path, plain_header, separate_header) as writer:
            for block in self.blockchain.get_blocks_in_range(start, end):
                writer.write(block)
                if progress:
                    processed_blocks = block.height - start + 1
                    last_percentage = ((processed_blocks - 1) * 100) // number_of_blocks
                    percentage = (processed_blocks * 100) // number_of_blocks
                    if percentage > last_percentage:
                        progress(processed_blocks / number_of_blocks)
        if separate_header:
            sort(output_path, 'addresses.csv', '-u')
            if deduplicate_transactions:
                for base_name in ['transactions', 'rel_tx_output',
                                  'outputs', 'rel_output_address']:
                    sort(output_path, base_name + '.csv', '-u')
