<style>
  .table-font {
    color: white;
  }
</style>

<script lang="ts">
  import { Link } from 'svelte-navigator';
</script>

<div class="table-font">
  <h1>Twitter Verification Public Tweet :: timestamp</h1>
  <h1>Instagram Verification Public Post :: timestamp</h1>
  <div class="px-2">
    <p>
      <b>timestamp</b> is a property of
      <Link to="/InstagramVerificationPublicPost"
        >Instagram Verification Public Post</Link
      > and <Link to="/TwitterVerificationPublicTweet"
        >Twitter Verification Public Tweet</Link
      >
    </p>
    <p>It is the timestamp of when the verification media was witnessed</p>
    <p>
      Expected to have the value of <a
        href="http://www.w3.org/2001/XMLSchema#dateTime">Datetime</a
      >
    </p>
  </div>
</div>
