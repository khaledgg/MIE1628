
public class KMeans {

	public static class PointsMapper extends Mapper<LongWritable, Text, Text, Text> {

		// centroids : Linked-list/arraylike

		@Override
		public void setup(Context context) {

			super.setup(context);
			Configuration conf = context.getConfiguration();

			// retrive file path
			Path centroids = new Path(conf.get("centroid.path"));

			// create a filesystem object
			FileSystem fs = FileSystem.get(conf);

			// create a file reader
			SequenceFile.Reader reader = new SequenceFile.Reader(fs, centroids, conf);

			// read centroids from the file and store them in a centroids variable
			Text key = new Text();
			IntWritable value = new IntWritable();
			while (reader.next(key, value)) {
				centers.add(new Point(key.toString()));
			}
			reader.close();

		}

		@Override
		public void map(LongWritable key, Text value, Context context) throws IOException, InterruptedException {

			// input -> key: charater offset, value -> a point (in Text)
			// write logic to assign a point to a centroid
			// emit key (centroid id/centroid) and value (point)

		}

		@Override
		public void cleanup(Context context) throws IOException, InterruptedException {

		}

	}

	public static class PointsReducer extends Reducer<Text, Text, Text, Text> {

		public static enum Counter {
			CONVERGED
		}
		// new_centroids (variable to store the new centroids

		@Override
		public void setup(Context context) {

		}

		@Override
		public void reduce(Text key, Iterable<Text> values, Context context) throws IOException, InterruptedException {
			// Input: key -> centroid id/centroid , value -> list of points
			// calculate the new centroid
			// new_centroids.add() (store updated cetroid in a variable)

		}

		@Override
		public void cleanup(Context context) throws IOException, InterruptedException {
			// BufferedWriter
			// delete the old centroids
			// write the new centroids

		}

	}

	public static void main(String[] args) throws Exception {

		Configuration conf = new Configuration();

		Path center_path = new Path("centroid/cen.seq");
		conf.set("centroid.path", center_path.toString());

		FileSystem fs = FileSystem.get(conf);

		if (fs.exists(center_path)) {
			fs.delete(center_path, true);
		}

		final SequenceFile.Writer centerWriter = SequenceFile.createWriter(fs, conf, center_path, Text.class,
				IntWritable.class);
		final IntWritable value = new IntWritable(0);
		centerWriter.append(new Text("50.197031637442876,32.94048164287042"), value);
		centerWriter.append(new Text("43.407412339767056,6.541037020010927"), value);
		centerWriter.append(new Text("1.7885358732482017,19.666057053079573"), value);
		centerWriter.append(new Text("32.6358540480337,4.03843047564191"), value);

		centerWriter.close();

		while (itr < 10) {
			// config
			// job
			// set the job parameters
			// itr ++
		}

		// read the centroid file from hdfs and print the centroids (final result)

	}

}